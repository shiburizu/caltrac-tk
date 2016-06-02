from Tkinter import *
import sqlite3 as sql

class mainWindow(Tk):
	def __init__(self):
		Tk.__init__(self)
		#calculator box
		self.fra1 = calcFrame = Frame(self)
		calcFrame.grid(row=0,column=0)
		self.foodlst = foodlst = Listbox(calcFrame)
		foodlst.grid(row=0,column=0)
		
		#user profile box
		self.fra2 = profileFrame = Frame(self)
		profileFrame.grid(row=0,column=1,sticky='N')
		self.inpAge = inpAge = Entry(profileFrame)
		inpAge.grid(row=0,column=0)
		
		
gui = mainWindow()
gui.mainloop()
