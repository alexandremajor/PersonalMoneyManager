import sqlite3
import Controls.spend as spend
import json
class Connection:
	"""
	Used to represent a connection to the database.
	Attributes:
		database(string):path to database
		connection(sqlite3.connection):connection object to database
		save_loc(string):path to location where csv files are stored
	"""
	def __init__(self):
		with open("conf.json") as conf:
			paths=json.load(conf)
		self.database=str(paths["DATABASE"])
		self.connection=sqlite3.connect(self.database)
		self.save_loc=str(paths["SAVE_LOCATION"])

	def write(self,entry):
		"""
		Spending -> None
		Writes a Spending object into the database.
		"""
		crsr=self.connection.cursor()
		sql_comm="INSERT INTO expenses VALUES ("+str(entry.amount)+", \""+str(entry.date)+"\", \""+str(entry.category)+"\", \""+str(entry.note)+"\");"
		crsr.execute(sql_comm)
		self.connection.commit()
	
	def get_last(self):
		"""
		None -> Spending
		Reads from the database the last written entry and returns it as a Spending object.
		"""
		crsr=self.connection.cursor()
		sql_comm="SELECT rowid,* FROM expenses ORDER BY rowid DESC LIMIT 1;"
		crsr.execute(sql_comm)
		newest=crsr.fetchall()
		s=spend.Spending(float(newest[0][1]),newest[0][2],newest[0][3],newest[0][4],newest[0][0])
		return s

	def read(self,date):
		"""
		list -> list
		Retrieves all entries between two dates from the database. Takes as input a list containing the two date endpoints (inclusive) and returns a list of spend objects.
		"""
		crsr=self.connection.cursor()
		sql_command="SELECT rowid,* FROM expenses WHERE date <= \'"+ str(date[1])+"\' and date >= \'"+str(date[0])+"\';"
		crsr.execute(sql_command)
		ans=crsr.fetchall()
		spend_list=[]
		for entry in ans:
			new_spend=spend.Spending(float(entry[1]),entry[2],entry[3],entry[4],entry[0])
			spend_list.append(new_spend)
		return spend_list

	def make_csv(self,data,name):
		"""
		Spending, str -> str
		Converts the Spending object into csv format string and writes it in a csv file. The function takes as input data, a Spending object, and name, the desired name for the csv file (without .csv extension).
		"""
		name=self.save_loc+str(name)+'.csv'
		f=open(name,'w+')
		for spend in data:
			f.write(spend.csv())
			f.write("\n")
		f.close()
		return name
	def __del__(self):
		"""
		None -> None
		Invoked when the object is destroyed. Closes the database connection.
		"""
		self.connection.close()
