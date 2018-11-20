
#!/usr/bin/python

import serial, string, time, sqlite3
from picamera import PiCamera
from threading import Thread
import MySQLdb
from keypad import Keypad
from RFIDReader import RFIDReader
from LCD import LCD

class SmartDoorLockSystem:
	def __init__(self):
		self.rfidReader = RFIDReader()
		self.keypad = Keypad()
		self.lcd = LCD()
		self.dbName = "allowedtags.db"
		self.correct_pin = "1234*"
		self.entered_pin = ""
		print('\nWelcome to the Smart Home Lock System\n')
		print('Scan an active RFID card or enter the correct pin to unlock the door\n')
	
	def connect_to_database(self):
		pass
	
	def main(self):
		while True:
			tagID = self.rfidReader.grab_rfid_data()
			if (tagID[0] != ""):
				#An RFID tag was scanned
				conn = sqlite3.connect('/home/pi/Desktop/allowedtags.db')
				c = conn.cursor()
				c.execute('SELECT * FROM  allowedtags WHERE tagID=?',tagID)
				if c.fetchone():
					self.lcd.setText('ACCESS GRANTED', 1)
					self.lcd.setText('Door Unlocked', 2)
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
							self.lcd.setText('Door Unlocked', 1)
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
