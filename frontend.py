from Tkinter import *
import ttk
from RS232 import *
import tkMessageBox as messagebox
import ImageTk



class Nexys_A7_interface():
        def __init__(self, window):
                self.window = window
                self.tab_control = ttk.Notebook(window)

                self.on = ImageTk.PhotoImage(file = "on.png")
                self.off = ImageTk.PhotoImage(file = "off.png")
                self.on_sw = ImageTk.PhotoImage(file = "sw_on.png")
                self.off_sw = ImageTk.PhotoImage(file = "sw_off.png")

                self.tab1 = Frame(self.tab_control)
                self.tab2 = Frame(self.tab_control)
                self.tab3 = Frame(self.tab_control)
                self.tab4 = Frame(self.tab_control)
                self.tab5 = Frame(self.tab_control)

                self.tab_control.add(self.tab1, text='Connection')
                self.tab_control.add(self.tab2, text='Leds')
                self.tab_control.add(self.tab3, text='Switches')
                self.tab_control.add(self.tab4, text='Sensors')
                self.tab_control.add(self.tab5, text='7 Seg')

                self.leds = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
                                
                self.connectionWindows()
                self.ledsWindows()
                self.swWindows()
                self.adSensorWindows()
                self.displaySegWindows()

                self.tab_control.pack(expand=1, fill='both')

                self.__hide_tabs()

                #RECOGER LAS VARIABLES AQUI 
                self.Nexys_A7 = Nexys_A7_RS232()
                self.is_connected = False

                #SW
                self.__fifo_check_thread = threading.Thread(target = self.__fifo_check)

#**************************  Connection **************************************************************************************************                

        def __hide_tabs(self):
                for i in range (1,5):
                        self.tab_control.hide(i)

        def __show_tabs(self):
                for i in range (1,6):
                        self.tab_control.add(getattr(self, "tab" + str(i)))

        def connectionWindows(self):
                label = Label(self.tab1, text="Connection:")
                label.grid(column=0, row=0)

                connection_type_label = Label(self.tab1, text="Connection Type:")
                connection_type_label.grid(column=3, row=1)

                self.conn_type = ttk.Combobox(self.tab1)
                self.conn_type.grid(column=4, row=1)
                self.conn_type.bind('<<ComboboxSelected>>', self.__conn_type_callback)
                self.conn_type["values"] = ("Serial")


                port_label = Label(self.tab1, text="Port:")
                port_label.grid(column=3, row=3)

                self.port = ttk.Combobox(self.tab1)
                self.port.grid(column=4, row=3)

                self.conn_btn = Button(self.tab1, text="CONNECT", command=self.btn_conn_disconn_clicked)
                self.conn_btn.grid(column=4, row=4)

        def btn_conn_disconn_clicked(self):
                if self.Nexys_A7.connect_disconnect(self.port.get()):
                        if self.is_connected:
                                self.conn_btn.configure(text = "Connect")
                                self.__stop_threads()
                                self.__hide_tabs()
                        else:
                                self.conn_btn.configure(text = "Disconnect")
                                self.__init_threads()
                                self.__show_tabs()

        def __init_threads(self):
                self.is_connected = True
                self.__fifo_check_thread.start()

        def __stop_threads(self):
                self.is_connected = False
                        

        def __conn_type_callback(self, event):
                if self.conn_type.get() == "Serial":
                        self.port["values"] = self.Nexys_A7.serial_ports

#**************************  Leds_Window **************************************************************************************************
                
        def ledsWindows(self):
                status_label = Label(self.tab2, text="STATUS")
                status_label.grid(column=0, row=0)

                self.btnleds = []
                j = 1           
                z = 0

                for i in range(16):
                        status_label = Label(self.tab2, text="LD" + str(i))
                        status_label.grid(column=z, row=j)

                        on_btn = Button(self.tab2, image=self.off, command=lambda i = i:self.switch(i))
                        on_btn.grid(column=z + 1, row=j)
                        
                        self.btnleds.append(on_btn)                                             
                        
                        j = j + 1                       
                        if j > 4: 
                                j = 1
                                z = z + 2
                                
                rgb_label = Label(self.tab2, text="RGB")
                rgb_label.grid(column=0, row=5)
                
                led_label = Label(self.tab2, text="LED")
                led_label.grid(column=0, row=6)
                self.__led_combobox = ttk.Combobox(self.tab2)
                self.__led_combobox.grid(column=1, row=6)
                self.__led_combobox["values"] = (0, 1)
                self.__led_combobox.set(0)
                
                red_label = Label(self.tab2, text="Red")
                red_label.grid(column=2, row=6)
                red_scale = ttk.Scale(self.tab2, from_ = 0, to = 255, command = lambda duty = 0, component = 0 : self.__rgb_callback(duty, component))
                red_scale.grid(column=3, row=6)
                
                green_label = Label(self.tab2, text="Green")
                green_label.grid(column=4, row=6)
                green_scale = ttk.Scale(self.tab2, from_ = 0, to = 255, command = lambda duty = 0, component = 1 : self.__rgb_callback(duty, component))
                green_scale.grid(column=5, row=6)
                
                blue_label = Label(self.tab2, text="Blue")
                blue_label.grid(column=6, row=6)
                blue_scale = ttk.Scale(self.tab2, from_ = 0, to = 255, command = lambda duty = 0, component = 2 : self.__rgb_callback(duty, component))
                blue_scale.grid(column=7, row=6)

        def __rgb_callback(self, duty, component):

                cmd = "P"
                ms_byte = (self.__led_combobox.current() << 2) + component
                ls_byte = int(float(duty))
                        
                cmd += chr(ms_byte) + chr(ls_byte)
                self.Nexys_A7.send_cmd(cmd)
                        
                
        def switch(self, btnNumber):    
                if self.leds[btnNumber]:
                        self.btnleds[btnNumber].config(image=self.off)
                        self.leds[btnNumber] = False
                else:       
                        self.btnleds[btnNumber].config(image=self.on)
                        self.leds[btnNumber] = True
                self.__leds_status_format()

        def __leds_status_format(self): 
                cmd = chr(76)
                ms_byte = 0
                ls_byte = 0
                for i in range (0,16):
                        if i < 8 :
                                if self.leds[i]:
                                        ms_byte = ms_byte << 1 | 1 
                                else:
                                        ms_byte = ms_byte << 1
                        else:
                                if self.leds[i]:
                                        ls_byte = ls_byte << 1 | 1 
                                else:
                                        ls_byte = ls_byte << 1
                
                cmd += chr(ms_byte) + chr(ls_byte)
                self.Nexys_A7.send_cmd(cmd)

#**************************  Switches Window **************************************************************************************************

        def swWindows(self):
                label = Label(self.tab3, text="SW:")
                label.grid(column=0, row=0)
                for i in range(16):
                        sw_label = Label(self.tab3, text="SW" + str(15-i))
                        sw_label.grid(column=i, row=2)

                        setattr(self, "sw_indicator" + str(i), Label(self.tab3, image = self.off_sw))
                        getattr(self,"sw_indicator" + str(i)).grid(column=i, row=1)
                
#**************************  Sensors Window **************************************************************************************************

        def adSensorWindows(self):
                label = Label(self.tab4, text="Sensores:")
                label.grid(column=0, row=0)

                temperatura_label = Label(self.tab4, text="Temperatura:")
                temperatura_label.grid(column=1, row=1)

                self.temperatura = Entry(self.tab4)
                self.temperatura.grid(column=2, row=1)
                

#**************************  7 seg Window **************************************************************************************************

        def displaySegWindows(self):
                label = Label(self.tab5, text="Segmentos:")
                label.grid(column=0, row=0)

                position_label = Label(self.tab5, text="Position:")
                position_label.grid(column=1, row=2)

                self.position = ttk.Combobox(self.tab5)
                self.position.grid(column=2, row=2)
                self.position["values"] = (0,1,2,3,4,5,6,7)


                data_label = Label(self.tab5, text="Data:")
                data_label.grid(column=1, row=4)
                self.data = Entry(self.tab5)
                self.data.grid(column=2, row=4)

                btn = Button(self.tab5, text="Send", command=self.btn_7seg_clicked)
                btn.grid(column=2, row=5)

        def btn_7seg_clicked(self):
                cmd = "D"
                ms_byte = self.position.get()
                ls_byte = self.data.get()
                cmd += ms_byte + ls_byte
                self.Nexys_A7.send_cmd(cmd)

#**************************  Nexys A7 info rcvd **************************************************************************************************

        def __fifo_check (self):
                while self.is_connected:
                        if self.Nexys_A7.cmd_rcvd_fifo.is_empty == False:
                                self.__decode(self.Nexys_A7.cmd_rcvd_fifo.read())

        def __decode(self, data_in):
                #print data_in
                sw_bin_array = ""
                if data_in[0] == 'S':
                        sw_status = str(data_in[1]) + str(data_in[2])
                        for in_bytes in sw_status:
                                in_bytes = format(ord(in_bytes), "b")
                                while len(in_bytes) < 8:
                                        in_bytes = "0" + in_bytes
                                sw_bin_array += in_bytes
                        for i in range(16):
                                if sw_bin_array[i] == "1":
                                        getattr(self, "sw_indicator" + str(i)).configure(image = self.on_sw)
                                else:
                                        getattr(self, "sw_indicator" + str(i)).configure(image = self.off_sw)

#**************************  Closing app **************************************************************************************************                    

        def on_closing(self):
                if messagebox.askokcancel("Quit", "Do you want to quit?"):
                        self.Nexys_A7.shut_down()
                        self.__stop_threads()
                        self.window.destroy()


if __name__ == '__main__':
        window = Tk()
        window.title('RS232')
        window.geometry('600x250+50+50')

        app = Nexys_A7_interface(window)

        
        window.protocol("WM_DELETE_WINDOW", app.on_closing)

        window.mainloop()


