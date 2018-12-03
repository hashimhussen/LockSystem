#!/usr/bin/python

#TODO Remove unused modules
import serial, string, time, sqlite3, socket
from picamera import PiCamera
from threading import Thread
#import MySQLdb
from Keypad import Keypad
from RFIDReader import RFIDReader
from LCD import LCD
from DoorLatch import DoorLatch
from UDP import UDP
from Button import Button
from Mock import Mock
from random import randint

class SmartDoorLockSystem:
	''' Smart Door Lock System Logic '''
	def __init__(self):
		''' Initialization code '''
		#TODO Remove Test Code
		self.testing = False
		self.busy = False

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
		
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.server_address = ('192.168.43.206', 8888)
		self.socket.bind(self.server_address)
		
		self.dbName = "allowedtags.db"
		self.correct_pin = "1234" #TODO get pin from database, instead of hardcoding
		self.entered_pin = ""


	def listen_for_messages(self):
		while True:
			buf, address = self.socket.recvfrom(2048)
			if len(buf):
				UDP.processMessage(buf,self.doorLatch)

	def main(self):
		print('\nWelcome to the Smart Home Lock System\n')
		print('Scan an active RFID card or enter the correct pin to unlock the door\n')

		t = Thread(target=self.listen_for_messages)
		t.daemon = True
		t.start()
		
		#Infinite Loop
		while True:
			if (self.busy != True):
				#Scan for an RFID card every iteration
				tagID = self.rfidReader.grab_rfid_data()
				
				#If the tagID returned was nothing (no tag was scanned)
				if (tagID[0] != ""): #tagID is a tuple
					
					self.busy = True
	
					#Connect to the database
					#TODO Move to initialization code
					conn = sqlite3.connect('/home/pi/Desktop/allowedtags.db')
					c = conn.cursor()
					
					#Search the database for the scanned tagID
					c.execute('SELECT * FROM  allowedtags WHERE tagID=?',tagID)
					
					#TODO Add logic for Master card
					
					#If the tagID was found in the database
					if c.fetchone():
						self.doorLatch.unlockDoor()
						self.lcd.setText('ACCESS GRANTED', 2)
						time.sleep(3)
						self.doorLatch.lockDoor()
					else:
						self.lcd.setText('ACCESS DENIED', 2)
						#TODO Log attempted access + time + RFID tag ID used
				
				#If a key was pressed on the keypad
				if (self.keypad.lastKeyPressed != ""):
					self.busy = True
					#Append the key to the pin being entered
					self.entered_pin = self.entered_pin + self.keypad.lastKeyPressed
					self.lcd.setText(self.entered_pin)
					
					#Cancel pin entry if the '#' button is pressed on the keypad
					if ((self.keypad.lastKeyPressed == '#')):
						self.lcd.setText("Cancelled PIN \nEntry",2)
						self.entered_pin = ""
						self.keypad.lastKeyPressed = ""
				
					if ((self.keypad.lastKeyPressed == '*')):			
						if ((len(self.entered_pin)-1) == len(self.correct_pin)):	
							#If the user entered the correct pin
							if (self.entered_pin[:-1] == self.correct_pin):
								#TODO add LED Logic
								self.doorLatch.unlockDoor()
								self.lcd.setText("Access Granted", 1)
								#self.lcd.setText('Door Unlocked', 1)
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
					elif (len(self.entered_pin) > len(self.correct_pin)):
						#Flash LED
						self.lcd.setText("Invalid PIN \nFormat", 2)
						self.entered_pin = ""
						self.keypad.lastKeyPressed = ""
	
					#Clear the lastKeyPressed on every iteration
					self.keypad.lastKeyPressed = ""

				#If the physical unlock button is pressed
				if (Button.isUnlockButtonPressed() and (self.doorLatch.status == "LOCKED")):
					self.doorLatch.unlockDoor()
					self.lcd.setText("Access Granted", 1)
					self.entered_pin = ""
					self.keypad.lastKeyPressed = ""		

				#If the physical lock button is pressed
				if (Button.isLockButtonPressed() and (self.doorLatch.status == "UNLOCKED")):
					self.doorLatch.lockDoor()
					self.entered_pin = ""
					self.keypad.lastKeyPressed = ""	


				self.rfidReader.ser.flushInput()
				self.busy = False


if __name__ == '__main__':
	#Initialize the Lock System and start running
	lock = SmartDoorLockSystem()
	lock.main()

	GPIO.cleanup()
