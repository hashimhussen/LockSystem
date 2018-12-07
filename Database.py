import mysql.connector

class Database(object):
	""" Networked MySQL Database """

	def __init__(self):
		""" Setup Database """
		
		self.mydb = mysql.connector.connect(
  		host="localhost", #Assign a static ip and put host IP here
  		user="root",
  		passwd="raspberry",
		database="lockSystem"
		)

		self.cursor = self.mydb.cursor()


	def getCorrectPin(self):
		"""
		Get the correct pin from the database at runtime

		Parameters
	    	----------
	    	None
		
		Returns
	    	-------
	    	pin : string
			The correct pin to unlock the door latch
		"""
		#Set and execute the MySQL command
		command = "SELECT pin FROM validpins"
		self.cursor.execute(command)
		
		#Get the pin
		pin = self.cursor.fetchone()
		#Return the pin if it exists, else return False
		if pin:
			return pin[0]
		else:
			return False


	def isTagInDatabase(self,tagID):
		"""
		Check if the scanned Tag ID is in the database
		
		Parameters
	    	----------
	    	tagID : string
			The ID of the scanned tag
		
		Returns
	    	-------
	    	tag : string
			The tagID corresponding to the scanned tag
		"""
		#Set and execute the MySQL command
		command = "SELECT * FROM validtags WHERE tag={}".format(tagID)
		self.cursor.execute(command)
		
		#Try to get the tag from the database
		tag = self.cursor.fetchone()
		
		#Return the tag if it exists, else return False
		if tag:
			return tag[0]
		else:
			return False


	def isMasterTag(self,tagID):
		"""
		Check if the scanned Tag ID corresponds to a master tag
		
		Parameters
	    	----------
	    	tagID : string
			The ID of the scanned tag
		
		Returns
	    	-------
	    	bool
			True if the scanned tag was a master tag, else returns False
		"""
		#Set and execute the MySQL command
		command = "SELECT * FROM validtags WHERE tag={} AND master=1".format(tagID)
		self.cursor.execute(command)
		
		#Check if the tag was in the database and was a master tag
		master = self.cursor.fetchone()
		
		#If the tag was indeed a master tag, return True, else return False
		if master:
			return True
		else:
			return False


	def addTagToDatabase(self,tagID):
		"""
		Add the tagID to the database
		
		Parameters
	    	----------
	    	tagID : string
			The ID of the scanned tag
		
		Returns
	    	-------
	    	None
		"""
		#Set and execute the MySQL command
		command = "INSERT INTO validtags (tag, master) VALUES ({}, 0)".format(tagID)
		self.cursor.execute(command)
		self.mydb.commit()

		#Test if tag was really added
		command = "SELECT * FROM validtags WHERE tag={} AND master=0".format(tagID)
		self.cursor.execute(command)
		tag = self.cursor.fetchone()
		#If the tag was added and found, return True, else return False
		if tag:
			return True
		else:
			return False


	def removeTagFromDatabase(self,tagID):
		"""
		Remove the tagID from the database
		
		Parameters
	    	----------
	    	tagID : string
			The ID of the scanned tag
		
		Returns
	    	-------
	    	None
		"""
		#Set and execute the MySQL command
		command = "DELETE FROM validtags WHERE tag={}".format(tagID)
		self.cursor.execute(command)
		self.mydb.commit()
		
		#Test if tag was really deleted
		command = "SELECT * FROM validtags WHERE tag={} AND master=0".format(tagID)
		self.cursor.execute(command)
		tag = self.cursor.fetchone()
		#If the tag was removed and not found, return True, else return False
		if tag:
			return False
		else:
			return True

	def logFailedAccess(self):
		"""
		Log the failed entry attempt
		
		Parameters
	    	----------
	    	None
		
		Returns
	    	-------
	    	None
		"""
		#Set and execute the MySQL command
		command = "INSERT INTO failed_access_times (time) VALUES (NOW())"
		self.cursor.execute(command)
		self.mydb.commit()
