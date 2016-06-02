
import easygui
import sqlite3 as sql
from Tkinter import *
import sys
from datetime import datetime, date

class mainWindow(Tk):
	def __init__(self):
		Tk.__init__(self)
		self.wm_title('CalTrac')
		self.buildMain()

	def buildMain(self):
		#calculator box
		self.fra1 = calcFrame = Frame(self)
		calcFrame.grid(row=0,column=0)
		self.foodscrl = foodscrl = Scrollbar(calcFrame)
		foodscrl.grid(row=1,column=3,sticky=NS)
		self.foodlbl = foodlbl = Label(calcFrame,text='FOOD')
		foodlbl.grid(row=0,column=0,sticky=W)
		self.foodlbl1 = foodlbl1 = Label(calcFrame,text='KCAL')
		foodlbl1.grid(row=0,column=1,sticky=W)
		
		self.foodlst = foodlst = Listbox(calcFrame,yscrollcommand=foodscrl.set)
		foodlst.grid(row=1,column=0)
		
		self.foodlst1 = foodlst1 = Listbox(calcFrame,yscrollcommand=foodscrl.set,width=10)
		foodlst1.grid(row=1,column=1)
		
		foodscrl.config(command=foodlst.yview)
		
		self.addFood = addFood = Button(calcFrame,text='Add Item',command=updateTracker)
		addFood.grid(row=2,column=0,sticky=W,pady=5,padx=5)

		#user profile box
		self.statvar = StringVar()
		self.kcalvar = StringVar()
		self.totalvar = StringVar()
		self.goalvar = StringVar()
		self.fra2 = profileFrame = Frame(self)
		profileFrame.grid(row=0,column=1,sticky=N,padx=5)
		self.dataLbl = dataLbl = Label(profileFrame,textvariable=self.statvar,justify=LEFT)
		dataLbl.grid(row=0,column=0)
		
		self.setupPro = setupPro = Button(profileFrame,
		text='Reconfigure',command=SetupProfile)
		setupPro.grid(row=1,column=0)
		
		self.fraWeight = fraWeight = Frame(self)
		fraWeight.grid(row=1,column=0)
		self.totalLbl = totalLbl = Label(fraWeight,textvariable=self.totalvar)
		totalLbl.grid(row=0,column=0,sticky=W)
		self.kcalLbl = kcalLbl = Label(fraWeight,textvariable=self.kcalvar)
		kcalLbl.grid(row=1,column=0,sticky=W)
		
		self.spnWeight = spnWeight = Spinbox(fraWeight,textvariable=self.goalvar,values=('Lose weight', 'Maintain weight', 'Gain weight'),command=self.checkSpn)
		self.goalvar.set('Maintain weight')
		spnWeight.grid(row=2,column=0)

	def checkSpn(self):
		t = self.spnWeight.get()
		print t
		if t.startswith('L'):
			if (profile.data['bmr'] - 500) < 1600:
				self.kcalvar.set('Daily recommended kcal intake: 1600')
			else:
				self.kcalvar.set('Daily recommended kcal intake: ' + str(int(profile.data['bmr'])-500))
		elif t.startswith('M'):
			self.kcalvar.set('Daily recommended kcal intake: ' + str(int(profile.data['bmr'])))
		elif t.startswith('G'):
			self.kcalvar.set('Daily recommended kcal intake: ' + str(int(profile.data['bmr'])+500))
		
	def listUpdate(self,l):
		self.foodlst.delete(0,END)
		self.foodlst1.delete(0,END)
		for it in l:
			self.foodlst.insert(END,'%s - x%s' % (it[0],str(it[3]).replace('.0','')))
			self.foodlst1.insert(END,str(it[2]).replace('.0',''))
	def getDailyFood(self):
		d = c.execute("SELECT * FROM foods WHERE date = ?", (date.isoformat(date.today()),)).fetchall()
		self.listUpdate(d)
		self.sumDailyFood()
	
	def sumDailyFood(self):
		t = list(c.execute("SELECT TOTAL(kcal) FROM foods WHERE date = ?",(date.isoformat(date.today()),)).fetchone())
		t = t[0]; t = int(t); self.totalvar.set('Total kcal intake today: %s' % t) #lol

class user(object):
	
	def usrProfile(self): #creates a dictionary of user data from SQLite
		self.p = c.execute('SELECT name,height,weight,age,gender,rating FROM user').fetchall()
		try:
			for i in self.p[0]:
				self.p.append(i)
			self.p.pop(0)
			self.p.extend(None for i in range(len(self.p),6))
			print self.p
		except IndexError:
			self.p = [None,None,None,None,None,None]
			SetupProfile(self)
		self.data = {'raw':self.p,'name':self.p[0],'height':self.p[1],
		'weight':self.p[2],'age':self.p[3],'gender':self.p[4],'rating':self.p[5]}
		if self.data['gender'] == 'Male':
			bmr = 88.362 + (13.397*self.data['weight']) + (4.799*self.data['height']) - (5.677*self.data['age'])
		elif self.data['gender'] == 'Female':
			bmr = 447.593 + (9.247*self.data['weight']) + (3.098*self.data['height']) - (4.330*self.data['age'])
		factors = [0,1.2,1.375,1.55,1.725,1.9]
		if self.data['rating'] != None:
			bmr = bmr*factors[self.data['rating']]
			self.data['bmr'] = bmr
			self.stats = "%s's profile\nGender:%s\nHeight:%s\nWeight:%s\nAge:%s\nRating:%s" % (
			self.data['name'],self.data['gender'],self.data['height'],self.data['weight'],
			self.data['age'],self.data['rating'])	
			gui.statvar.set(self.stats)
			gui.kcalvar.set('Daily recommended kcal intake: ' + str(int(self.data['bmr'])))
		else:
			sys.exit(0)
	def __init__(self):
		self.usrProfile()
		print self.data # testing purposes

#the functions below operate outside of the objects and can't run as funcs of user.
def SetupProfile(o=None): #handles the GUI setup process
	msg = 'Profile Creation'
	title = 'CalTrac'
	genders = ['Male','Female']
	genderslct = easygui.boolbox(msg,title,genders)
	fieldNames = ['Name','Height', 'Weight', 'Age']
	fieldValues = easygui.multenterbox(msg,title,fieldNames)
	try:
		if fieldValues is None and None in profile.p:
			sys.exit(0)
		elif '' not in fieldValues:
			rateMsg = """How would you describe the amount of exercise you do?
	1. Little to no exercise
	2. Light exercise(1-3 days per week)
	3. Moderate exercise(3-5 days per week)
	4. Heavy exercise(6-7 days per week)
	5. Very heavy exercise(twice per day, extra heavy workouts)"""
			exercise = easygui.enterbox(rateMsg)
			if exercise != None:
				if o == None:
					updateProfile(fieldValues,exercise,genderslct)
				else:
					updateProfile(fieldValues,exercise,genderslct,o)
			elif None in profile.p:
				sys.exit(0)
		else:
			easygui.msgbox('One or more values were not valid. Please try again')
	except TypeError:
		pass

def updateProfile(u,e,g,o=None): #makes sure all of the data goes in to SQLite correctly and sanity checks
	try:
		if g == 1:
			g = 'Male'
		elif g == 0:
			g = 'Female'
		inp = [u[0],float(u[1]),float(u[2]),int(u[3]),g,int(e)]
		print inp
		c.execute("INSERT OR REPLACE INTO user(func,name,height,weight,age,gender,rating) VALUES('USER',?,?,?,?,?,?);",
		(inp[0],inp[1],inp[2],inp[3],inp[4],inp[5]))
		db.commit()
		if o == None:		
			profile.usrProfile() #fetches said data back from SQLite to ensure accuracy
		else:
			o.usrProfile()
	except ValueError:
		easygui.msgbox('One or more values were not valid. Please try again')

def updateTracker():
	addItemNames = ['Name','Kcal','Portion']
	addItem = easygui.multenterbox('ADD NEW SERVING','CalTrac',addItemNames)
	try:
		t = date.today()
		if addItem != None or '':
			realKcal = int(addItem[1]) * int(addItem[2])
			c.execute("INSERT INTO foods(name,date,kcal,portion) VALUES(?,?,?,?);",
			(addItem[0],t,realKcal,int(addItem[2])))
			db.commit()
		else:
			pass #error checking todo?
		#pull from db
		gui.getDailyFood()
	except ValueError:
		print 'error'

db = sql.connect('CalTrac.db',detect_types=sql.PARSE_DECLTYPES)
c = db.cursor()
#TODO error checking
c.execute('''CREATE TABLE IF NOT EXISTS user(func TEXT UNIQUE, name TEXT,
 height REAL, weight REAL, age INTEGER, gender TEXT	, rating INTEGER);''')
c.execute('''CREATE TABLE IF NOT EXISTS foods(name TEXT, date DATE, kcal REAL, 
portion REAL);''')
gui = mainWindow()
profile = user()
gui.getDailyFood()
gui.mainloop()
