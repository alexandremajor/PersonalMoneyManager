from abc import ABC,abstractmethod
import tkinter as tk
import Controls.spend as spend
import Database.connection as conn
import re
import datetime
import os
class Mode(ABC):
	"""
	Abstract class representing a possible mode the application is in.
	Attributes:
		session(Session): session object which created the current mode.
		frame(tk.Frame): tkinter frame displaying the mode.
		readables(list): list of widgets which receive user input.
	"""
	def __init__(self,session):
		self.session=session
		self.frame=None
		self.readables=[]
		self.create_widgets()
		self.create_master_controls()

	def create_master_controls(self):
		"""
		None -> None
		Creates controls common to all modes (quit application, go back home screen).
		"""
		#create buttons
		back=tk.Button(self.frame,text="Cancel and return main menu",command=lambda:self.session.switch(0),height=1,width=20)
		quit=tk.Button(self.frame,text="Quit",command=lambda:self.session.end(),height=1,width=20)
		#pack buttons in frame
		back.pack()
		quit.pack()
	
	@abstractmethod
	def create_widgets(self):
		"""
		None -> None
		Creates widgets and packs them in the frame.
		"""
		pass
	
	def read(self):
		"""
		None -> list
		Retrieves user inout in readable widgets (self.readables).	
		"""
		val=[]
		for w in self.readables:
			val.append(w.get())
		return val
	
	def reset(self):
		"""
		None -> None
		Resets all readables widgets (self.readables).
		"""
		for i in self.readables:
			i.set("")
	def activate(self):
		"""
		None -> None
		Activates the mode by placing its frame in session window.
		"""
		self.frame.place(relx=0.5,rely=0.5,anchor='center')


class IntroMode(Mode):
	"""
	Used to represent the mode corresponding to the home screen of the session window.
	Inherits from Mode.
	Attributes:
		None
	"""
	def __init__(self,session):
		super().__init__(session)		


	def create_widgets(self):
		self.frame=tk.Frame(self.session.window)
		widgets=[]
		title=tk.Label(self.frame,text="Personal Finance Manager",font=("Helvetica",45))
		question=tk.Label(self.frame,text="Which operation would you like to perform?",font=("Helvetica",20))
		entry=tk.Button(self.frame,text="Enter new entries",command=lambda:self.session.switch(1),height=2,width=30)
		retrieve=tk.Button(self.frame,text="Retrieve data",command=lambda:self.session.switch(2),height=2,width=30)
		widgets.extend((title,question,entry,retrieve))
		for i in widgets:
			i.pack()
			

class EntryMode(Mode):
	"""
	Represents the mode used to add new expenses to the databse.
	Inherits from Mode.
	Attributes:
		None		
	"""
	def __init__(self,session):
		super().__init__(session)

	def create_widgets(self):
		self.frame=tk.Frame(self.session.window)
		label=tk.Label(self.frame,text="Enter the information below:",font=("Helvetica",25))
		#amount entry
		amount=tk.Label(self.frame,text="Amount spent:")
		amount_in=tk.StringVar()
		amount_entry=tk.Entry(self.frame,textvariable=amount_in)
		#date drop menus (day,month,year)
		date=tk.Label(self.frame,text="Date:")
		day_in=tk.StringVar()
		day=tk.OptionMenu(self.frame,day_in,*list(map(lambda y:y.zfill(2),[str(number) for number in range(1,32)])))
		month_in=tk.StringVar()
		month=tk.OptionMenu(self.frame,month_in,*list(map(lambda y:y.zfill(2),[str(number) for number in range(1,13)])))
		current=int(datetime.datetime.now().year)
		year_in=tk.StringVar()
		year=tk.OptionMenu(self.frame,year_in,*list(map(lambda y:y.zfill(2),[str(year) for year in range(current-2,current+1)])))
		#category drop menu
		category=tk.Label(self.frame,text="Category:")
		cat_in=tk.StringVar()
		cat_entry=tk.OptionMenu(self.frame,cat_in,"1. Rent","2.Groceries","3. Services","4. Entertainment","5. Food","6. Other")
		#note entry field
		note=tk.Label(self.frame,text="Note (optional):")
		note_in=tk.StringVar()
		note_entry=tk.Entry(self.frame,textvariable=note_in)
		#submit button
		submit=tk.Button(self.frame,text="Submit",command=lambda:self.get_entry())
		#pack widgets
		widgets=[]
		widgets.extend((label,amount,amount_entry,date,day,month,year,category,cat_entry,note,note_entry,submit))
		self.readables.extend((amount_in,day_in,month_in,year_in,cat_in,note_in))
		for w in widgets:
			w.pack()

	def get_entry(self):
		"""
		None -> None
		Reads the user input, if valid, writes it to the database,
		displays a message in a popup window and resets the input widgets..
		"""
		val=self.read()
		mess=tk.StringVar()
		try:
			self.validate(val)
			new_entry=spend.Spending(float(val[0]),val[3]+"-"+val[2]+"-"+val[1],val[4],val[5])	
			self.session.connection.write(new_entry)
			mess.set("Successfully submitted!")
		except Exception as e:
			mess.set(e)
		self.session.popup(mess)
		self.reset()

	def validate(self,val):
		"""
		list -> None
		Validates the user input contained in val.
		Raises:
			AttributeError: if a field contains an invalid value
		"""
		pattern1=re.compile('^[0-9]+$')	
		pattern2=re.compile('^[0-9]+[.][0-9]+$')
		if not(pattern1.match(val[0]) or pattern2.match(val[0])):
			self.readables[0].set("")
			raise AttributeError("Invalid format for amount. Expected int or float.")
		if "" in (val[1],val[2],val[3]):
			raise AttributeError("Please select a date.")
		if ""==val[4]:
			raise AttributeError("Please select a category.")			

class DataMode(Mode):
	"""
	Represents the mode used to retrieve past expenses from the database.
	Inherits from Mode.
	Attributes:
		None
	"""
	def __init__(self,session):
		super().__init__(session)

	def create_widgets(self):
		self.frame=tk.Frame(self.session.window)
		#instructions label
		instruction=tk.Label(self.frame,text="Enter the information below:",font=("Helvetica",25))
		#beginning date
		current=int(datetime.datetime.now().year)
		beg=tk.Label(self.frame,text="Enter the beginning date:",font=("Helvetica",15))
		beg_day_in=tk.StringVar()
		beg_day=tk.OptionMenu(self.frame,beg_day_in,*list(map(lambda y:y.zfill(2),[str(number) for number in range(1,32)])))
		beg_month_in=tk.StringVar()
		beg_month=tk.OptionMenu(self.frame,beg_month_in,*list(map(lambda y:y.zfill(2),[str(number) for number in range(1,13)])))
		beg_year_in=tk.StringVar()
		beg_year=tk.OptionMenu(self.frame,beg_year_in,*[str(year) for year in range(current-3,current+1)])

		#end date
		end=tk.Label(self.frame,text="Enter the end  date:",font=("Helvetica",15))
		end_day_in=tk.StringVar()
		end_day=tk.OptionMenu(self.frame,end_day_in,*list(map(lambda y:y.zfill(2),[str(number) for number in range(1,32)])))
		end_month_in=tk.StringVar()
		end_month=tk.OptionMenu(self.frame,end_month_in,*list(map(lambda y:y.zfill(2),[str(number) for number in range(1,13)])))
		end_year_in=tk.StringVar()
		end_year=tk.OptionMenu(self.frame,end_year_in,*[str(year) for year in range(current-3,current+1)])
	
		#select graph option
		graph_in=tk.StringVar()
		graph=tk.Checkbutton(self.frame,text="Produce barplot?",variable=graph_in,onvalue="G",offvalue="")
		
		#get latest option
		latest=tk.Button(self.frame,text="See latest submitted entry",command=self.get_latest)

		#submit button
		submit=tk.Button(self.frame,text="Submit",command=self.get_dates)
		#pack widgets
		wid=[]
		wid.extend((instruction,beg,beg_day,beg_month,beg_year,end,end_day,end_month,end_year,graph,latest,submit))
		for i in wid:
			i.pack()
		self.readables.extend((beg_day_in,beg_month_in,beg_year_in,end_day_in,end_month_in,end_year_in,graph_in))

	def get_dates(self):
		"""
		None -> None
		Retrieves user input and, if valid, produces csv file with desired values.
		If barplot option selected, invokes R script to produce the plot.
		Finally, displays success message in popup window.
		"""
		val=self.read()
		mess=tk.StringVar()
		try:
			self.validate(val)
			beg=val[2]+"-"+val[1]+"-"+val[0]
			end=val[5]+"-"+val[4]+"-"+val[3]
			dates=[beg,end]
			entries=self.session.connection.read(dates)
			name=beg+"_to_"+end
			self.session.connection.make_csv(entries,name)
			if val[6]=="G":
				os.system("Controls/Visualizer.r "+self.session.connection.save_loc+name)
			mess.set("Successfully completed!")	
		except Exception as e:
			mess.set(e)
		self.session.popup(mess)
		self.reset()		

	def validate(self,val):
		"""
		list -> None
		Validates the user input contained in val.
		Raises:
			AttributeError: if invalid input entered by the user
		"""
		for i in val[0:7]:
			if i=="":
				raise AttributeError("Please specify all fields for the dates.")
		beg=datetime.datetime(int(val[2]),int(val[1]),int(val[0]))
		end=datetime.datetime(int(val[5]),int(val[4]),int(val[3]))
		if (beg>end) or (beg>datetime.datetime.now()):
			raise AttributeError("The dates entered are invalid.")				
		
	def get_latest(self):
		"""
		None -> None
		Retrieves the last entered expense in the database and displays it in a popup window.
		"""
		last=self.session.connection.get_last()
		text=tk.StringVar()
		text.set(last.__str__())
		self.session.popup(text)
