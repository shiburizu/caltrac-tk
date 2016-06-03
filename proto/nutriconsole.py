class User(object):
	def __init__(self):
		self.Gender = 'male'
		self.Height = None
		self.Weight = None
		self.Age = None
		self.BMR = None
		self.kcal = None
	def createProfile(self, genderchoice):
		self.Gender = genderchoice
		print "Enter your weight in kg."
		self.Weight = float(raw_input('>>: '))
		print "Enter your height in cm."
		self.Height = float(raw_input('>>: '))
		print "Enter your age in years."
		self.Age = int(raw_input('>>: '))
		#BMR calc	
		if self.Gender == 'male':
			self.BMR = 88.362 + (13.397*self.Weight) + (4.799*self.Height) - (5.677*self.Age)
		elif self.Gender == 'female':
			self.BMR = 447.593 + (9.247*self.Weight) + (3.098*self.Height) - (4.330*self.Age)
		print """How would you describe the amount of exercise you do?
1. Little to no exercise
2. Light exercise(1-3 days per week)
3. Moderate exercise(3-5 days per week)
4. Heavy exercise(6-7 days per week)
5. Very heavy exercise(twice per day, extra heavy workouts)"""
		multiplier = int(raw_input('>>: '))
		self.kcal = self.BMR * factors[multiplier]
		print "Your daily recommended kcal intake is: ", self.kcal

factors = [1.2,1.375,1.55,1.725,1.9]
profile = User()

print "Are you male or female?"
genderchoice = raw_input(">>: ")

if genderchoice == 'male' or 'male' in genderchoice:
	profile.createProfile('male')
elif genderchoice == 'female' or 'female' in genderchoice:
	profile.createProfile('female')
	

