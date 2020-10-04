import threading, time
import serial
import string

class SerThread:
    def __init__(self, port=0):
        self.my_serial = serial.Serial()
        self.my_serial.port = port
        self.my_serial.baudrate = 9600
        self.my_serial.timeout = 1
        self.alive = False
        fname = time.strftime('%Y%m%d_%H_%M_%S')    #file name
        self.rfname = 'r' + fname
        self.sfname = 's' + fname
        self.thread_read = None
        self.thread_send = None
        self.waitEnd = None     # thread event

    def waiting(self):
        if self.waitEnd is not None:
            self.waitEnd.wait()
    def start(self):
        self.rfile = open(self.rfname, 'w')
        self.sfile = open(self.sfname, 'w')
        self.my_serial.open()

        if self.my_serial.isOpen():
            self.waitEnd = threading.Event()
            self.alive = True
            self.thread_read = threading.Thread(target=self.thread_read)
            self.thread_read.setDaemon(True)
            self.thread_send = threading.Thread(target=self.thread_send)
            self.thread_send.setDaemon(True)
            self.thread_read.start()
            self.thread_send.start()

            return True
        else:
            return False

    def reader(self):
        while self.alive:
            try:
                n = self.my_serial.inWaiting()
                data = ''
                if n:
                    data = self.my_serial.read(n)
                    hex_data = [hex(i) for i in data]
                    print('recv ' + time.strftime('%Y-%m-%d %X:') + hex_data)
                    print(time.strftime("%Y-%m-%d %X:") + hex_data, file=self.rfile)

                    if len(data) == 1 and data[len(data)-1] is 'q':
                        break
            except Exception as e:
                print(e)

        self.waitEnd.set()
        self.alive = False
    
    def sender(self):
        while self.alive:
            try:
                send_data = input('input data:\n')
                self.my_serial.write(send_data)
                print('sent ' + time.strftime('%Y-%m-%d %X') )
                print(send_data, file=self.sfile)

            except  Exception as e:
                print(e)

        send.waitEnd.set()
        send.alive = False

    def stop(self):
        



