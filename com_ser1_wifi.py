import serial
from serial.serialutil import EIGHTBITS, PARITY_EVEN, STOPBITS_ONE
import serial.tools.list_ports
import threading
from queue import Queue
import time
import os
from serial import Serial


class SerialObject:
    def __init__(self, port='com10', baudrate=9600):
        self.serial = serial.Serial()
        self.serial.port = port
        self.serial.baudrate = baudrate
        self.serial.timeout = 2
        self.serial.parity = PARITY_EVEN
        self.serial.stopbits = STOPBITS_ONE
        self.serial.bytesize = EIGHTBITS
    
    
class SerialApp:
    def __init__(self, master_com='com41', slave_com='com42'):
        # two usart spy
        self.serial_spy_master = None
        self.serial_spy_slave = None
        # file path
        self.sfile_path = ''
        # thread wait event
        self.wait = None
        self.alive = False
        # two spy usart object
        self.spy_sobj_master = SerialObject(master_com)
        self.spy_sobj_slave = SerialObject(slave_com)
        # spy usart, command, file thd
        self.serialspy_master_rx_thd = None
        self.serialspy_master_tx_thd = None
        self.serialspy_slave_tx_thd = None
        self.serialspy_slave_rx_thd = None
        self.command_thd = None
        self.file_thd = None

    # show exits coms
    def selec_coms(self, strs):
        com_list = list(serial.tools.list_ports.comports())
        for i in com_list:
            print(str(i))
        # manual select input coms
        input_com = input('input: select {} coms in the blow list coms .\n'.format(strs))
        return input_com

    def bind_port(self):
        # bind two ports
        self.serial_spy_master = self.spy_sobj_master
        port = self.selec_coms('master')
        if port is not '':
            self.serial_spy_master.serial.port = port
        print('your select {} com is {}'.format('master', self.serial_spy_master.serial.port))
        
        self.serial_spy_slave = self.spy_sobj_slave
        port = self.selec_coms('slave')
        if port is not '':
            self.serial_spy_slave.serial.port = port

        print('your select {} com is {}'.format('slave', self.serial_spy_slave.serial.port))

    def create_dir(self):
        # create dir
        cur_path = os.getcwd() + '/save/'
        
        if not os.path.exists(cur_path):
            os.makedirs(cur_path)
        self.sfile_path = cur_path + time.strftime('%Y-%m-%d %H-%M-%S') + '.txt'
        print(self.sfile_path)

    def read(self, ser_com: Serial, ser_que: Queue, file_que: Queue):
        '''
        read serial,
        send to ser_queue
        send to file_queue
        '''
        data = b''
        while self.alive:
            try:
                # read unitl number of data is 0 in every 0.1s
                time.sleep(0.05)
                n = ser_com.in_waiting
                if n:
                    data += ser_com.read(n)
                #n = ser_com.in_waiting
                if len(data) and n == 0:
                    datas = time.ctime() + ' ' + ser_com.port + ' rcv: ' + self.bytes_to_hexstring(data)
                    print(datas)
                    # if data is exit then exit the program
                    if data == b'exit':
                        break

                    # send to tx que
                    ser_que.put(data, 1)
                    # send to file que
                    file_que.put(datas, 1)
                    data = b''

            except Exception as e:
                print('read err')
                print(e)
                
        self.wait.set()
        self.alive = False
        print('read exit')
    
    def send_command(self, ser_master_que: Queue, ser_slave_que: Queue, file_que: Queue):
        '''
        read input command
        send to write_queue
        '''
        while self.alive:
            try:
                strs = input()
                # if command is 'exit' then exit
                if strs == 'exit':
                    break
                datas = strs.split(':')
                # print(datas[0])
                # print(self.spy_sobj_master.serial.port)
                # print(type(self.spy_sobj_master.serial.port))
                # if command send to master port
                if (datas[0] == self.spy_sobj_master.serial.port):
                    cmd = self.hex_to_bytes(datas[1])
                    ser_master_que.put(cmd)
                # if command send to slave port
                elif (datas[0] == self.spy_sobj_slave.serial.port):
                    cmd = self.hex_to_bytes(datas[1])
                    ser_slave_que.put(cmd)
                else:
                    print('unknow command')
                # save comands to file que
                f_data = time.ctime() + ' command-- ' + strs
                print(f_data)
                file_que.put(f_data, 1)
            except Exception as e:
                print('command err')
                print(e)

        self.wait.set()
        self.alive = False
        print('command exit')
        
    def send(self, ser_com: Serial, ser_que: Queue):
        '''
        read queue
        write serial
        '''
        while self.alive:
            try:
                send_data = ser_que.get(1)
                ser_com.write(send_data)
                ser_que.task_done()
            except Exception as e:
                print('send err')
                print(e)
        self.wait.set()
        self.alive = False
        print('send exit')


    def ser_thread(self, func, ser_com: Serial, read_que: Queue, file_que: Queue):
        # create rx thd
        ser_com.open()
        print('{} is open'.format(ser_com.port))
        thd = threading.Thread(target=func, args=(ser_com, read_que, file_que,))
        thd.setDaemon(True)
        return thd

    def save_file(self, file_que: Queue, file_path):
        '''
        read que
        save file
        '''
        while self.alive:
            try:
                with open(file_path, 'a') as f:
                    data = file_que.get(1)
                    # d = time.ctime() + ' Rcv:' + self.bytes_to_hexstring(data)
                    #print(d)
                    f.writelines(data + '\n')
                    file_que.task_done()
            except Exception as e:
                print('write err')
                print(e)
        print('file exit')

    def waiting(self):
        if self.wait is not None:
            self.wait.wait()

    def start(self):
        # bind port
        # create dir
        self.bind_port()
        self.create_dir()
        try:
            # set thd alive to true
            self.alive = True
            self.wait = threading.Event()

            # init queue
            self.serialspy_master_rx_que = Queue()
            self.serialspy_slave_tx_que = Queue()
            self.save_file_queue = Queue()

            # master serial spy thread
            self.serialspy_master_rx_thd = self.ser_thread(self.read,
                    self.serial_spy_master.serial, self.serialspy_master_rx_que, self.save_file_queue)

            self.serialspy_master_tx_thd = threading.Thread(target=self.send, args=(self.serial_spy_master.serial, self.serialspy_master_rx_que,))
            
            # slave serial spy thread
            self.serialspy_slave_rx_thd = self.ser_thread(self.read,
                    self.serial_spy_slave.serial, self.serialspy_slave_tx_que, self.save_file_queue)

            self.serialspy_slave_tx_thd = threading.Thread(target=self.send, args=(self.serial_spy_slave.serial, self.serialspy_slave_tx_que,))

            # command thd
            self.command_thd = threading.Thread(target=self.send_command, args=(self.serialspy_master_rx_que, self.serialspy_slave_tx_que, self.save_file_queue,))
            self.command_thd.setDaemon(True)

            # file thd
            self.file_thd = threading.Thread(target=self.save_file, args=(self.save_file_queue, self.sfile_path))
            self.file_thd.setDaemon(True)

            # thd start
            self.serialspy_master_rx_thd.start()
            print('master rx thd start')

            self.serialspy_master_tx_thd.setDaemon(True)
            self.serialspy_master_tx_thd.start()
            print('master tx thd start')

            self.serialspy_slave_rx_thd.start()
            print('slave rx thd start')

            self.serialspy_slave_tx_thd.setDaemon(True)
            self.serialspy_slave_tx_thd.start()
            print('slave tx thd start')

            self.command_thd.start()
            print('command thd start')

            self.file_thd.start()
            print('file thd start')


        except Exception as e:
            self.alive = False
            self.wait.set()
            print(e)

    def serial_close_port(self, ser_com: Serial):
        # close port
        if ser_com.is_open:
            ser_com.close()
            print('{} is closed'.format(ser_com.port))

    def stop(self):
        self.alive = False
        self.serial_close_port(self.serial_spy_master.serial)
        self.serial_close_port(self.serial_spy_slave.serial)
        

    def string_to_bytes(self, strs):
        '''
        string to bytes
        eg:
        '0123456789ABCDEF0123456789ABCDEF'
        b'0123456789ABCDEF0123456789ABCDEF'
        '''
        return bytes(strs, encoding='utf8')

    def bytes_to_str(self, bs):
        '''
        bytes to string
        eg:
        b'0123456789ABCDEF0123456789ABCDEF'
        '0123456789ABCDEF0123456789ABCDEF'
        '''
        return bytes.decode(bs, encoding='utf-8')
    
    def bytes_to_hexstring(self, strs):
        '''
        bytes to hex string 
        eg:
        b'\x01#Eg\x89\xab\xcd\xef\x01#Eg\x89\xab\xcd\xef'
        '01 23 45 67 89 AB CD EF 01 23 45 67 89 AB CD EF'
        '''
        return ' '.join(['%02X' % b for b in strs])
        
    def hex_to_bytes(self, hexs):
        '''
        hex string to bytes
        eg:
        '01 23 45 67 89 AB CD EF 01 23 45 67 89 AB CD EF'
        b'\x01#Eg\x89\xab\xcd\xef\x01#Eg\x89\xab\xcd\xef'

        '''
        strs = hexs.replace(" ", "")
        return bytes.fromhex(strs)


if __name__ == "__main__":
    s = SerialApp()
    try:
        s.start()
        s.waiting()
        s.stop()
    except Exception as e:
        print(e)
    
