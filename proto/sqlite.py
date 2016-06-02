from Tkinter import *
import sqlite3 as sql

class gui(Tk):
    def __init__(self): 
		self.setupP = None
		Tk.__init__(self)
		self.ls = Listbox(self)
		self.ls.grid(row=0,column=0)
		
		self.entry = Entry(self)
		self.entry.grid(row=1,column=0)
		
		self.inb = Button(self,text="ENTER",command=insert)
		self.inb.grid(row=2,column=0)
		
		self.setupIn = Entry(self)
		self.setupIn.grid(column=1,row=0,sticky=N)
		
		self.setupOk = Button(self)
		self.setupOk.grid(row=1,column=1)
		
class dbhandle(object):
    pass
class user(object):
    pass
def Main():
	db.execute('''CREATE TABLE IF NOT EXISTS item (NAME CHAR(10));''')
	fetch = db.execute("SELECT * FROM item")
	db.commit()
	if fetch != None:
		app.ls.delete(0, END)
		for row in fetch:
			app.ls.insert(END, row[0])
def insert():
    db.execute("INSERT INTO item VALUES (%r);" % app.entry.get())
    db.commit()
    Main()

db = sql.connect('nutrition.db')
app = gui()
Main()
app.mainloop()

