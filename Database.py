import mysql.connector

class Database(object):
	""" Networked MySQL Database """

	def __init__(self):
		""" Setup Database """
		
		self.mydb = mysql.connector.connect(
  		host="localhost",
  		user="root",
  		passwd="raspberry",
		database="lockSystem"
		)

		self.cursor = self.mydb.cursor()


	def getCorrectPin(self):
		command = "SELECT pin FROM validpins"
		self.cursor.execute(command)
		pin = self.cursor.fetchone()
		if pin:
			return pin[0]
		else:
			return False


	def isTagInDatabase(self,tagID):
		command = "SELECT * FROM validtags WHERE tag={}".format(tagID)
		self.cursor.execute(command)
		tag = self.cursor.fetchone()
		if tag:
			return tag[0]
		else:
			return False


	def isMasterTag(self,tagID):
		command = "SELECT * FROM validtags WHERE tag={} AND master=1".format(tagID)
		self.cursor.execute(command)
		master = self.cursor.fetchone()
		if master:
			return True
		else:
			return False


	def addTagToDatabase(self,tagID):
		command = "INSERT INTO validtags (tag, master) VALUES ({}, 0)".format(tagID)
		self.cursor.execute(command)
		self.mydb.commit()

		#Test if tag was really added
		command = "SELECT * FROM validtags WHERE tag={} AND master=0".format(tagID)
		tag = self.cursor.fetchone()
		if tag:
			return True
		else:
			return False


	def removeTagFromDatabase(self,tagID):
		command = "DELETE FROM validtags WHERE tag={}".format(tagID)
		self.cursor.execute(command)
		self.mydb.commit()
		
		#Test if tag was really deleted
		command = "SELECT * FROM validtags WHERE tag={} AND master=0".format(tagID)
		tag = self.cursor.fetchone()
		if tag:
			return False
		else:
			return True