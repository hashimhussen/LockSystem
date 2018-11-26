#!/usr/bin/python

#TODO Remove unused modules
import serial, string, time, sqlite3
from picamera import PiCamera
from threading import Thread
import MySQLdb
from keypad import Keypad
from RFIDReader import RFIDReader
from LCD import LCD
from DoorLatch import DoorLatch
from Mock import Mock
from random import randint

class SmartDoorLockSystem:
	''' Smart Door Lock System Logic '''
	def __init__(self):
		''' Initialization code '''
		#TODO Remove Test Code
		self.testing = True
		
		#If not in debug mode, initialize real hardware
		if not self.testing:
			self.rfidReader = RFIDReader()
			self.keypad = Keypad()
			self.lcd = LCD()
			self.doorLatch = DoorLatch()
		#If in debug mode, initialize Mock hardware
		else:
			self.rfidReader = Mock.RFIDReader()
			self.keypad = Mock.Keypad()
			self.lcd = Mock.LCD()
			self.doorLatch = Mock.DoorLatch()
		
		self.dbName = "allowedtags.db"
		self.correct_pin = "1234" #TODO get pin from database, instead of hardcoding
		self.entered_pin = ""
	
	def main(self):
		#print('\nWelcome to the Smart Home Lock System\n')
		#print('Scan an active RFID card or enter the correct pin to unlock the door\n')
		
		#Infinite Loop
		while True:
			#TODO Remove test code
			if self.testing:
				time.sleep(2)
				tagID = self.rfidReader.grab_rfid_data()
				time.sleep(1)
				#Generate a random number and simulate a button press
				self.keypad.lastKeyPressed = str(randint(0,9))
				if (len(self.entered_pin) == 4):
					self.keypad.lastKeyPressed = '*'
			else:
				#Scan for an RFID card every iteration
				tagID = self.rfidReader.grab_rfid_data()
				
			#If the tagID returned was nothing (no tag was scanned)
			if (tagID[0] != ""): #tagID is a tuple
				
				#Connect to the database
				#TODO Move to initialization code
				conn = sqlite3.connect('/home/pi/Desktop/allowedtags.db')
				c = conn.cursor()
				
				#Search the database for the scanned tagID
				c.execute('SELECT * FROM  allowedtags WHERE tagID=?',tagID)
				
				#TODO Add logic for Master card
				
				#If the tagID was found in the database
				if c.fetchone():
					self.lcd.setText('ACCESS GRANTED', 1)
					#self.lcd.setText('Door Unlocked', 2)
					self.doorLatch.unlockDoor()
					#TODO Change sleep time accordingly
					time.sleep(2)
					self.doorLatch.lockDoor()
				else:
					self.lcd.setText('ACCESS DENIED', 2)
					#TODO Log attempted access + time + RFID tag ID used
			
			#If a key was pressed on the keypad
			if (self.keypad.lastKeyPressed != ""):
				#Append the key to the pin being entered
				self.entered_pin = self.entered_pin + self.keypad.lastKeyPressed
				self.lcd.setText(self.entered_pin)
				
				#Cancel pin entry if the '#' button is pressed on the keypad
				if ((self.keypad.lastKeyPressed == '#')):
					self.lcd.setText("Cancelled PIN \nEntry",2)
					self.entered_pin = ""
					self.keypad.lastKeyPressed = ""
				
				if (len(self.entered_pin) == len(self.correct_pin)):
					if ((self.keypad.lastKeyPressed == '*')):
						#If the user entered the correct pin
						if (self.entered_pin == self.correct_pin):
							#TODO add LED Logic
							self.lcd.setText("Access Granted", 1)
							#self.lcd.setText('Door Unlocked', 1)
							self.doorLatch.unlockDoor()
							time.sleep(2)
							self.doorLatch.lockDoor()
							self.entered_pin = ""
							self.keypad.lastKeyPressed = ""
						#If the user entered the incorrect pin
						else:
							self.lcd.setText("Access Denied", 2)
							self.entered_pin = ""
							self.keypad.lastKeyPressed = ""
					#If the user entered pin is longer than the correct pin
					else:
						self.lcd.setText("Invalid PIN \nFormat", 2)
						self.entered_pin = ""
						self.keypad.lastKeyPressed = ""
						
				#If the user entered pin is shorter than the correct pin
				elif ((self.keypad.lastKeyPressed == '*')):
					#Flash LED
					self.lcd.setText("Invalid PIN \nFormat", 2)
					self.entered_pin = ""
					self.keypad.lastKeyPressed = ""

				#Clear the lastKeyPressed on every iteration
				self.keypad.lastKeyPressed = ""



if __name__ == '__main__':
	#Initialize the Lock System and start running
	lock = SmartDoorLockSystem()
	lock.main()
