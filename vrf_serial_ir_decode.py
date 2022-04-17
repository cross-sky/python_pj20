'''
Author: your name
Date: 2021-11-12 11:42:42
LastEditTime: 2021-12-25 19:42:39
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \serial\e1_serial.py
'''
import threading, time
import serial
import serial.tools.list_ports
import string
import rd505_ir

def strToBytes(str):
    '''
    '001122334455' -> b'001122334455'
    '''
    return bytes(str, encoding='utf8')

def bytesToStr(bs):
    '''
    b'001122334455'  -> '001122334455'
    '''
    return bytes.decode(bs, encoding='utf8')

def hexstringToBytes(str):
    '''
    '00 11 22 33 44 55' -> b'\x00\x11\x22\x33\x44\x55'
    '''
    return bytes.fromhex(str)

def bytesToHexstring(bs):
    '''
    b'\x00\x11\x22\x33\x44\x55' -> '00 11 22 33 44 55'  
    '''
    return ''.join(['%02X ' % b for b in bs])


class SerThread:
    def __init__(self, port=None):
        self.my_serial = serial.Serial()
        self.my_serial.port = port
        self.my_serial.baudrate = 9600
        self.my_serial.timeout = 1
        self.alive = False
        fname = time.strftime('%Y%m%d_%H_%M_%S')    #file name
        self.rfname = r'myserial/' + fname + '.txt'
        self.thread_read = None
        self.thread_send = None
        self.waitEnd = None     # thread event

    def waiting(self):
        if self.waitEnd is not None:
            self.waitEnd.wait()
    def start(self):
        self.rfile = open(self.rfname, 'w', encoding='utf8')
        #print(time.strftime("%Y-%m-%d %X: ") + 'haha', file=self.rfile, flush=False)
        self.rfile.writelines(time.strftime("%Y-%m-%d %X: ") + 'haha')
        self.rfile.flush()

        ports = list(serial.tools.list_ports.comports())
        if len(ports) <= 0:
            print("The serial port can't find! ")
            return False
        else:
            print("Open : {}".format(ports[-1]))
            self.my_serial.port = list(ports[-1])[0]
            self.my_serial.close()

            if not self.my_serial.isOpen():
                self.my_serial.open()

        #self.my_serial.open()

        if self.my_serial.isOpen():
            print('start threading')
            self.waitEnd = threading.Event()
            self.alive = True
            self.thread_read = threading.Thread(target=self.reader)
            self.thread_read.setDaemon(True)
            self.thread_send = threading.Thread(target=self.sender)
            self.thread_send.setDaemon(True)
            self.thread_read.start()
            self.thread_send.start()
            self.thread_read.join()
            self.thread_send.join()

            return True
        else:
            return False

    def reader(self):
        irdecode = rd505_ir.Rd505IrProcess()
        data = b''
        while self.alive:
            try:
                time.sleep(0.05)
                n = self.my_serial.inWaiting()
                if n:
                    data += self.my_serial.read(n)
                if len(data) and n == 0:
                    # -2 means the end of received data is useless 
                    hex_data = bytesToHexstring(data[:-1])
                    irdecode.decode_ir(hex_data)

                    print('recv ' + time.strftime('%Y-%m-%d %X: ') + hex_data)
                    print(irdecode.irdict)
                    self.rfile.writelines('recv ' +time.strftime("%Y-%m-%d %X: ") + hex_data + '\r\n')
                    self.rfile.writelines(str(irdecode.irdict) + '\r\n')
                    self.rfile.flush()
                    data = b''
                    
            except Exception as e:
                print('read error: ')
                print( e )
        print('reader exit')
        self.waitEnd.set()
        self.alive = False
    
    def sender(self):
        while self.alive:
            try:
                send_data = input('input data:\n')

                if len(send_data) == 1 and send_data[0] == 'q':
                    break
                    
                #print('s: ' + send_data)
                data_bytes = hexstringToBytes(send_data)
                self.my_serial.write(data_bytes)
                print('sent ' + time.strftime('%Y-%m-%d %X ') + send_data)
                #print(time.strftime("%Y-%m-%d %X: ") + 'haha', file=self.rfile, flush=False)
                #print('sent ' + time.strftime("%Y-%m-%d %X: ") + send_data, file=self.rfile, flush=False)
                self.rfile.writelines('sent ' + time.strftime("%Y-%m-%d %X: ") + send_data + '\r\n')
                self.rfile.flush()

            except  Exception as e:
                print(e)
        print('send exit')
        self.waitEnd.set()
        self.alive = False

    def stop(self):
        self.rfile.close()
        #self.sfile.close()
        self.waitEnd.set()
        self.alive = False


if __name__ == "__main__":
    s = SerThread()
    try:
        s.start()
    finally:
        s.stop()
    print('end')
    
        
        



