
#!/usr/bin/python

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
	def __init__(self):
		self.testing = True
		if not self.testing:
			self.rfidReader = RFIDReader()
			self.keypad = Keypad()
			self.lcd = LCD()
			self.doorLatch = DoorLatch()
		else:
			self.rfidReader = Mock.RFIDReader()
			self.keypad = Mock.Keypad()
			self.lcd = Mock.LCD()
			self.doorLatch = Mock.DoorLatch()	
		self.dbName = "allowedtags.db"
		self.correct_pin = "1234*"
		self.entered_pin = ""
		print('\nWelcome to the Smart Home Lock System\n')
		print('Scan an active RFID card or enter the correct pin to unlock the door\n')
	
	def connect_to_database(self):
		pass
	
	def main(self):
		while True:
			if self.testing:
				time.sleep(2)
				tagID = self.rfidReader.grab_rfid_data()
				time.sleep(1)
				self.keypad.lastKeyPressed = str(randint(0,9))
				if (len(self.entered_pin) == 4):
					self.keypad.lastKeyPressed = '*'
			else:
				tagID = self.rfidReader.grab_rfid_data()
			if (tagID[0] != ""):
				#An RFID tag was scanned
				conn = sqlite3.connect('/home/pi/Desktop/allowedtags.db')
				c = conn.cursor()
				c.execute('SELECT * FROM  allowedtags WHERE tagID=?',tagID)
				if c.fetchone():
					self.lcd.setText('ACCESS GRANTED', 1)
					#self.lcd.setText('Door Unlocked', 2)
					self.doorLatch.unlockDoor()
					time.sleep(2)
					self.doorLatch.lockDoor()
					#Log attempted access + time + RFID tag ID used
				else:
					self.lcd.setText('ACCESS DENIED', 2)
			if (self.keypad.lastKeyPressed != ""):
				self.entered_pin = self.entered_pin + self.keypad.lastKeyPressed
				self.lcd.setText(self.entered_pin)
				if ((self.keypad.lastKeyPressed == '#')):
					self.lcd.setText("Cancelled PIN \nEntry",2)
					self.entered_pin = ""
					self.keypad.lastKeyPressed = ""

				if (len(self.entered_pin) == len(self.correct_pin)):
					if ((self.keypad.lastKeyPressed == '*')):
						if (self.entered_pin == self.correct_pin):
							#unlockDoor()
							#Turn on Green LED
							#Wait 10 seconds
							#Turn off Green LED
							#lockDoor()
							self.lcd.setText("Access Granted", 1)
							#self.lcd.setText('Door Unlocked', 1)
							self.doorLatch.unlockDoor()
							time.sleep(2)
							self.doorLatch.lockDoor()
							self.entered_pin = ""
							self.keypad.lastKeyPressed = ""
						else:
							self.lcd.setText("Access Denied", 2)
							self.entered_pin = ""
							self.keypad.lastKeyPressed = ""
					else:
						#Flash Red LED
						self.lcd.setText("Invalid PIN \nFormat", 2)
						self.entered_pin = ""
						self.keypad.lastKeyPressed = ""
				elif ((self.keypad.lastKeyPressed == '*')):
					#Flash LED
					self.lcd.setText("Invalid PIN \nFormat", 2)
					self.entered_pin = ""
					self.keypad.lastKeyPressed = ""

				#Have to clear the lastKeyPressed otherwise we just re-enter the loop
				self.keypad.lastKeyPressed = ""



if __name__ == '__main__':
	lock = SmartDoorLockSystem()
	lock.main()
#conn = sqlite3.connect('/home/pi/Desktop/allowedtags.db')
#c = conn.cursor()
#output = " "
#ser = serial.Serial('/dev/ttyACM0', 9600)


#while True:
#  print "----"
#  while output != "":
#    tagID = (ser.readline(),)
#    c.execute('SELECT * FROM  allowedtags WHERE tagID=?',tagID)
#    exists = c.fetchone()
#
#    if exists:
#	print "ACCESS GRANTED"
#    else:
#        print "ACCES DENIED"
#
