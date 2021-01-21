import sqlite3
import Controls.spend as spend
import json
class Connection:
	def __init__(self):
		with open("conf.json") as conf:
			paths=json.load(conf)
		self.database=str(paths["DATABASE"])
		self.connection=sqlite3.connect(self.database)
		self.save_loc=str(paths["SAVE_LOCATION"])

	def write(self,entry):
		crsr=self.connection.cursor()
		sql_comm="INSERT INTO expenses VALUES ("+str(entry.amount)+", \""+str(entry.date)+"\", \""+str(entry.category)+"\", \""+str(entry.note)+"\");"
		crsr.execute(sql_comm)
		self.connection.commit()
	
	def get_last(self):
		crsr=self.connection.cursor()
		sql_comm="SELECT rowid,* FROM expenses ORDER BY rowid DESC LIMIT 1;"
		crsr.execute(sql_comm)
		newest=crsr.fetchall()
		s=spend.Spending(float(newest[0][1]),newest[0][2],newest[0][3],newest[0][4],newest[0][0])
		return s

	def read(self,date):
		"""
		list -> list
		Returns a list of spend objects in a list.
		"""
		crsr=self.connection.cursor()
		sql_command="SELECT rowid,* FROM expenses WHERE date < \'"+ str(date[1])+"\' and date > \'"+str(date[0])+"\';"
		crsr.execute(sql_command)
		ans=crsr.fetchall()
		spend_list=[]
		for entry in ans:
			new_spend=spend.Spending(float(entry[1]),entry[2],entry[3],entry[4],entry[0])
			spend_list.append(new_spend)
		return spend_list

	def make_csv(self,data,name):
		name=self.save_loc+str(name)+'.csv'
		f=open(name,'w+')
		for spend in data:
			f.write(spend.csv())
			f.write("\n")
		f.close()
		return name
	def __del__(self):
		self.connection.close()
