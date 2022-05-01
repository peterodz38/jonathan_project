from tkinter import *
from tkinter.ttk import *




class RS232():
	def __init__(self, window):
		self.window = window
		self.tab_control = Notebook(window)

		self.on = PhotoImage(file = "on.png")
		self.off = PhotoImage(file = "off.png")

		self.tab1 = Frame(self.tab_control)
		self.tab2 = Frame(self.tab_control)
		self.tab3 = Frame(self.tab_control)
		self.tab4 = Frame(self.tab_control)
		self.tab5 = Frame(self.tab_control)

		self.tab_control.add(self.tab1, text='Connection')
		self.tab_control.add(self.tab2, text='Leds')
		self.tab_control.add(self.tab3, text='S/W')
		self.tab_control.add(self.tab4, text='A/D Sensor')
		self.tab_control.add(self.tab5, text='7 Seg')

		self.leds = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
				
		self.connectionWindows()
		self.ledsWindows()
		self.swWindows()
		self.adSensorWindows()
		self.displaySegWindows()

		self.tab_control.pack(expand=1, fill='both')

		#RECOGER LAS VARIABLES AQUI 



	def connectionWindows(self):
		label = Label(self.tab1, text="Connection:")
		label.grid(column=0, row=0)

		connection_type_label = Label(self.tab1, text="Connection Type:")
		connection_type_label.grid(column=3, row=1)

		self.conn_type = Combobox(self.tab1)
		self.conn_type.grid(column=4, row=1)
		self.conn_type["values"] = (1,2,3, "OTRA")


		port_label = Label(self.tab1, text="Port:")
		port_label.grid(column=3, row=3)

		self.port = Combobox(self.tab1)
		self.port.grid(column=4, row=3)
		self.port["values"] = (1,2,3, "OTRA")

		btn = Button(self.tab1, text="CONNECT - DISCONNECT", command=self.btn_conn_disconn_clicked)
		btn.grid(column=4, row=4)

		
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

		
		
	def switch(self, btnNumber):	
		if self.leds[btnNumber]:
			self.btnleds[btnNumber].config(image=self.off)
			self.leds[btnNumber] = False
		else:       
			self.btnleds[btnNumber].config(image=self.on)
			self.leds[btnNumber] = True


	def swWindows(self):
		pass
		


	def adSensorWindows(self):
		label = Label(self.tab4, text="Sensores:")
		label.grid(column=0, row=0)

		temperatura_label = Label(self.tab4, text="Temperatura:")
		temperatura_label.grid(column=1, row=1)

		self.temperatura = Entry(self.tab4)
		self.temperatura.grid(column=2, row=1)
		


	def displaySegWindows(self):
		label = Label(self.tab5, text="Segmentos:")
		label.grid(column=0, row=0)

		position_label = Label(self.tab5, text="Position:")
		position_label.grid(column=1, row=2)

		self.position = Combobox(self.tab5)
		self.position.grid(column=2, row=2)
		self.position["values"] = (1,2,3,4,5,6,7)


		data_label = Label(self.tab5, text="Data:")
		data_label.grid(column=1, row=4)
		self.data = Entry(self.tab5)
		self.data.grid(column=2, row=4)

		btn = Button(self.tab5, text="OK", command=self.btn_seg_clicked)
		btn.grid(column=2, row=5)

	



	def btn_seg_clicked(self):
		pass

	def btn_conn_disconn_clicked(self):
		pass

		

		
	



def main():
	window = Tk()
	window.title('RS232')
	window.geometry('600x250+50+50')

	app = RS232(window)

	window.mainloop()


main()



