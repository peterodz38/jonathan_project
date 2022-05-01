from Tkinter import *
import ttk
import serial
import sys
import glob
import re
import threading


# Font configuration
Font_style='Times'
xlarge_text_size = 90
large_text_size = 40
medium_text_size = 20
small_text_size = 14
xsmall_text_size = 4

def serial_ports():
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

class FullscreenWindow:

    def connect_disconnect(self):
        try:
            if self.connection_succed == False:
                self.new_connection = serial.Serial(self.COM_ports[self.available_com_combobox.current()])
                self.new_connection.baudrate = 115200
                self.new_connection.timeout = 1
                self.connection_listening_thread_running = True
                self.connection_listening_thread.start()
                self.connect_btn.configure(text="Desconectar")
                self.connection_succed = True
                self.data_receive_lbl.configure(text='Conexion abierta en ' + self.new_connection.name)
                self.send_btn.configure(state='active')
            else:
                self.connection_listening_thread_running = False
                self.new_connection.close()
                self.connect_btn.configure(text="Conectar")
                self.data_receive_lbl.configure(text='Conexion finalizada')
                self.connection_succed = False
                self.send_btn.configure(state='disabled')
        except serial.SerialException:
            self.data_receive_lbl.configure(text='Error al conectar en ' + self.new_connection.name)

    # ***************codigo usado etapa de prueba***********************
    def send_serial(self):
        data = self.entry_code.get()
        #********************* Escritura **************************
        self.new_connection.write(data)

    #********************** Hilo de Lectura ***************************
    def read_byte (self):
        while self.connection_listening_thread_running:
            reading = self.new_connection.read()
            
            if reading != '':
                self.__cmd_rcvd[self.__bytes_counter] = reading
                self.__bytes_counter += 1
                
                if self.__bytes_counter == 3:
                    self.__bytes_counter = 0
                    self.decode_cmd(self.__cmd_rcvd)
                    
                #self.data_receive_lbl.configure(text= "Temp" + str(reading))
    # ******************************************************************

    def decode_cmd (self, cmd):
        if cmd[0] == 'T':
            temp = ord(cmd[1]) + ord(cmd[2]) * 0.0078
            #print str(temp) + '\n'
        if cmd[0] == 'S':
            pass
            #print 'S' + str(ord(cmd[1])) + str(ord(cmd[2])) + '\n'
        
    
    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background='gray')
        self.tk.title("RS232_Test")
        self.topFrame = Frame(self.tk)
        self.topFrame.pack(side = TOP, fill = BOTH, expand = YES)
        self.bottomFrame = Frame(self.tk)
        self.bottomFrame.pack(side = BOTTOM, fill = BOTH, expand = YES)
        self.COM_ports = serial_ports()
        self.available_com_combobox = ttk.Combobox(self.topFrame, width=20, font=(Font_style, small_text_size), values=self.COM_ports)
        self.available_com_combobox.grid(column=0,row=0,padx=10)
        self.entry_code = Entry(self.topFrame, width=20, font=(Font_style, small_text_size), fg="black", bg="white")
        self.entry_code.grid(column=0,row=1,stick='nswe',padx=10, pady=10)
        self.entry_code.insert(0,'')
        self.connect_btn = Button (self.topFrame, font=(Font_style, small_text_size), fg="black", bg="white", text="Conectar",
                                        width=10, command=self.connect_disconnect)
        self.connect_btn.grid(column=1,row=0,stick='nswe',padx=10, pady=10)
        self.send_btn = Button (self.topFrame, font=(Font_style, small_text_size), fg="black", bg="white", text="Enviar",
                                command=self.send_serial, state='disabled')
        self.send_btn.grid(column=1,row=1,stick='nswe',padx=10, pady=10)
        self.data_receive_lbl = Label(self.tk, width=20, font=(Font_style, small_text_size), fg="black", bg="white")
        self.data_receive_lbl.grid(column=0,row=2,stick='nswe',columnspan=2,padx=10,pady=10)

        self.new_connection = None
        self.connection_succed = False

        self.connection_listening_thread = threading.Thread(target = self.read_byte)
        self.connection_listening_thread_running = False

        self.__cmd_rcvd = [0,0,0]
        self.__bytes_counter = 0
        
if __name__ == '__main__':
    MainWindow = FullscreenWindow()
    MainWindow.tk.mainloop()
