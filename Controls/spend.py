class Spending:
	def __init__(self,amount,date,category,note="",key=None):
		self.amount=amount
		self.date=date
		self.category=category
		self.note=note
		self.key=key
	def __str__(self):
		return str(self.amount)+"$ on "+str(self.date)+" in category "+str(self.category)
	def csv(self):
		return str(self.amount)+","+str(self.date)+","+str(self.category)
	def __cmp__(self,other):
		return self.amount>other.amount
	def full(self):
		return self.__str__()+" with id "+str(self.key)

def create_spend():
	while(True):
		x=input()
		if (x=="n"):
			return None;
		try:

			amount=float(input("What is the amount spent?:"))
			if (amount <= 0):
				raise AttributeError("The amount can only be positive!")
			date=input("What date?")
			if (len(date)!=5 or date[2]!="/"):
				raise AttributeError("The date format is invalid.")
			print("Categories:\n1. Groceries\n2. Rent\n3. Services\n4. Food\n5. Entertainment\n6. Others")
			category=int(input("Choose one category above (number only):"))
			if not category in (1,2,3,4,5,6):
				raise AttributeError("Invalid category.")
			note=input("Enter an optional note:")
			return Spending(amount,date,category,note)
		except Exception as e:
			print(e)		
