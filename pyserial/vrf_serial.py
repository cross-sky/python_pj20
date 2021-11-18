'''
Author: your name
Date: 2021-11-12 11:42:42
LastEditTime: 2021-11-12 16:22:02
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \serial\e1_serial.py
'''
import threading, time
import serial
import serial.tools.list_ports
import string

from seria_a.serial_a import MySerial

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
        self.rfname = 'r' + fname + '.txt'
        self.sfname = 's' + fname + '.txt'
        self.thread_read = None
        self.thread_send = None
        self.waitEnd = None     # thread event

    def waiting(self):
        if self.waitEnd is not None:
            self.waitEnd.wait()
    def start(self):
        self.rfile = open(self.rfname, 'w')
        self.sfile = open(self.sfname, 'w')

        ports = list(serial.tools.list_ports.comports())
        if len(ports) <= 0:
            print("The serial port can't find! ")
            return False
        else:
            print("Open : {}".format(ports[-1]))
            
            #self.my_serial = serial.Serial(ports[-1], self.my_serial.baudrate)
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
        while self.alive:
            try:
                time.sleep(0.2)
                n = self.my_serial.inWaiting()
                data = ''
                if n:
                    data = self.my_serial.read(n)
                    if len(data) == 1 and data[0] == 'q':
                        break
                    
                    hex_data = bytesToHexstring(data)

                    #print('r '  + hex_data)
                    #hex_data = [hex(i) for i in data]

                    print('recv ' + time.strftime('%Y-%m-%d %X: ') + hex_data)
                    print(time.strftime("%Y-%m-%d %X: ") + hex_data, file=self.rfile)

                    
            except Exception as e:
                print(e)
        print('send exit')
        self.waitEnd.set()
        self.alive = False
    
    def sender(self):
        while self.alive:
            try:
                send_data = input('input data:\n')
                #print('s: ' + send_data)
                data_bytes = hexstringToBytes(send_data)
                self.my_serial.write(data_bytes)
                print('sent ' + time.strftime('%Y-%m-%d %X ') + send_data)
                print(time.strftime("%Y-%m-%d %X: ") + send_data, file=self.sfile)

            except  Exception as e:
                print(e)
        print('send exit')
        self.waitEnd.set()
        self.alive = False

    def stop(self):
        self.rfile.close()
        self.sfile.close()
        self.waitEnd.set()
        self.alive = False


if __name__ == "__main__":
    s = SerThread()
    try:
        s.start()
    finally:
        s.stop()
    print('end')
    
        
        



