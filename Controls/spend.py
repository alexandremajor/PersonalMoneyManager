class Spending:
	"""
	Used to represent a single spending.
	Attributes:
		amount(float):amount of money of the expense
		date(string):date of the expense (DD/MM/YYYY)
		category(string):category of the expense
		note(string):optional description
		key(int):unique ID (rowid in databse when retrieved, otherwise None)
	"""
	def __init__(self,amount,date,category,note="",key=None):
		self.amount=amount
		self.date=date
		self.category=category
		self.note=note
		self.key=key
	def __str__(self):
		"""
		None -> str
		Returns a string representation of the object.
		"""
		return str(self.amount)+"$ on "+str(self.date)+" in category "+str(self.category)
	def csv(self):
		return str(self.amount)+","+str(self.date)+","+str(self.category)
	def __cmp__(self,other):
		"""
		Spending -> boolean
		Compares two Spending objects according to their amounts.
		"""
		return self.amount>other.amount
	def full(self):
		"""
		None -> str
		Returns a string representation of the object with every attribute.
		"""
		return self.__str__()+" with id "+str(self.key)


