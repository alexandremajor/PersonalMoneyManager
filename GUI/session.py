import tkinter as tk
import Database.connection
import GUI.modes as modes
class Session:
	"""
	Represents the current session activated when starting the program.
	Controls the transition between the different modes of the program and manages the popup windows.
	Attributes:
		window(tk.Tk): main window
		connection(Database.connection.Connection): connection to database
		current_mode(GUI.Mode.Mode): current mode activated in the session
		modes(list): list of mode switchable to by the session	
	"""
	def __init__(self):
		self.window=tk.Tk()
		self.window.minsize(800,600)
		self.connection=Database.connection.Connection()
		self.current_mode=None
		self.modes=[]
		self.initialize()

	def initialize(self):
		"""
		None -> None
		Creates the possible modes for the session and launches the
		home menu (InitialMode). 
		"""
		home=modes.IntroMode(self)
		entry=modes.EntryMode(self)
		retrieve=modes.DataMode(self)
		self.modes.extend((home,entry,retrieve))
		self.switch(0)
	def switch(self,mode_pos):
		"""
		int -> None
		Switches the mode, updating the display on the screen.
		The int mode_pos corresponds to the position of the mode in the list self.modes.
		in self.modes.
		"""
		if (self.current_mode != None):
			self.current_mode.reset()
			self.current_mode.frame.place_forget()
		self.current_mode=self.modes[mode_pos]
		self.current_mode.activate()

	def end(self):
		"""
		None -> None
		Destroys the session window, effectively ending the program.
		"""
		self.window.destroy()
	
	def popup(self,message):
		"""
		None -> None
		Creates a popup window on top of the session window.
		"""	
		ConfirmationWindow(self.window,message)

class ConfirmationWindow(tk.Toplevel):
	"""
	Represents a popup window.
	Inherits from tk.TopLevel.
	Attributes:
		None
	"""
	def __init__(self,master,message):
		tk.Toplevel.__init__(self,master)
		tk.Label(self,textvariable=message).pack()
		tk.Button(self,text="Ok!",command=self.disable).pack()
		self.transient(master)
		self.grab_set()
	
	def disable(self):
		"""
		None -> None
		Destroys the popup window.
		"""
		self.grab_release()
		self.destroy()

