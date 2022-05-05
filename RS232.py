import serial
import sys
import glob
import re
import threading

class Nexys_A7_RS232:

    def __init__(self):

        self.serial_ports = self.__serial_ports()

        # serial connection
        self.__new_connection = None
        self.__connection_succed = False

        self.__connection_listening_thread = threading.Thread(target = self.__read_byte)
        self.__connection_listening_thread_running = False

        self.__cmd_rcvd = [0,0,0]
        self.__bytes_counter = 0

        # data managment
        #self.new_cmd_flag = False
        self.cmd_rcvd_fifo = FIFO()
        self.__bytes_counter = 0


    def __read_byte (self):
        while self.__connection_listening_thread_running:
            reading = self.__new_connection.read()
            
            if reading != '':
                self.__cmd_rcvd[self.__bytes_counter] = reading
                self.__bytes_counter += 1
                
                if self.__bytes_counter == 3:
                    self.__bytes_counter = 0
                    self.cmd_rcvd_fifo.insert(self.__cmd_rcvd)

            #self.new_cmd_flag = True

    def send_cmd (self, cmd):
        self.__new_connection.write(cmd)


    def connect_disconnect (self, serial_port):
        try:
            if self.__connection_succed == False:
                self.__new_connection = serial.Serial(serial_port)
                self.__new_connection.baudrate = 115200
                self.__new_connection.timeout = 1
                self.__connection_listening_thread_running = True
                self.__connection_listening_thread.start()
                self.__connection_succed = True
                return True
            else:
                self.__connection_listening_thread_running = False
                self.__new_connection.close()
                self.__connection_succed = False
                return True
        except serial.SerialException:
            return False


    def __serial_ports (self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def scan_serial_ports (self):
        self.serial_ports = self.__serial_ports()
        return self.serial_ports

    def shut_down (self):
        self.cmd_rcvd_fifo.fifo_stop()
        if self.__connection_succed:
            self.__new_connection.close()
            self.__connection_succed = False
            self.__connection_listening_thread_running = False
        

class FIFO:

    def __init__(self):

        self.__fifo_array = []

        self.is_empty = True
        
        self.__is_empty_thread = threading.Thread(target = self.__is_empty)
        self.__is_empty_thread_running = True
        #self.__is_empty_thread.start()
        
    def fifo_stop(self):
        self.__is_empty_thread_running = False

    def insert (self, data):
        
        self.__fifo_array.append(data)
        self.is_empty = False

    def read (self):

        data = self.__fifo_array.pop(0)
        if len(self.__fifo_array) == 0:
            self.is_empty = True
        else:
            self.is_empty = False
        return data

    def __is_empty (self):
        while self.__is_empty_thread_running:
            
            if len(self.__fifo_array) == 0:
                self.is_empty = True
            else:
                self.is_empty = False


