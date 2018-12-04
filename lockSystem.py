#!/usr/bin/python

import RPi.GPIO as GPIO
import time, socket
from threading import Thread
from Database import Database
from Keypad import Keypad
from RFIDReader import RFIDReader
from LCD import LCD
from DoorLatch import DoorLatch
from UDP import UDP
from Button import Button

class SmartDoorLockSystem:
	''' Smart Door Lock System Logic '''
	def __init__(self):
		''' Initialization code '''
		self.busy = False
		self.masterMode = False

		#Initialize system components
		self.rfidReader = RFIDReader()
		self.keypad = Keypad()
		self.lcd = LCD()
		self.doorLatch = DoorLatch()
		self.database = Database()

		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.server_address = ('192.168.43.206', 8888)
		self.socket.bind(self.server_address)
		
		self.correct_pin = self.database.getCorrectPin()
		self.entered_pin = ""


	def listen_for_messages(self):
		while True:
			buf, address = self.socket.recvfrom(2048)
			if len(buf):
				UDP.processMessage(buf,self.doorLatch)

	def updateDoorStatusInApp(self):
		host = "192.168.43.1"
		port = 8888
		target_address = (host,port)
		data = self.doorLatch.status
		self.socket.sendto(data.encode('utf-8'), target_address)

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

					#TODO Add logic for Master card
					if (self.database.isMasterTag(tagID[0])):
						if (self.masterMode):
							self.lcd.setText('')
							self.masterMode = False
							time.sleep(1)
						else:
							self.lcd.setText('MASTER MODE')
							self.masterMode = True
							time.sleep(1)
					
					else:
						if (self.masterMode):
							if (self.database.isTagInDatabase(tagID[0])):
								if (self.database.removeTagFromDatabase(tagID[0])):
									self.lcd.setText('TAG DEACTIVATED', 2)
								else:
									self.lcd.setText('FAILED TO \nDEACTIVATE TAG', 2)
							else:
								if (self.database.addTagToDatabase(tagID[0])):
									self.lcd.setText('TAG ACTIVATED', 2)
								else:
									self.lcd.setText('FAILED TO \nACTIVATE TAG', 2)
						else:
							#If a NORMAL tag was scanned and was found in the database
							if self.database.isTagInDatabase(tagID[0]):
								self.doorLatch.unlockDoor()
								self.lcd.setText('ACCESS GRANTED', 2)
								time.sleep(3)
								self.doorLatch.lockDoor()
							else:
								self.lcd.setText('ACCESS DENIED', 2)
								self.database.logFailedAccess()
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
								self.lcd.setText("ACCESS GRANTED", 2)
								time.sleep(3)
								self.doorLatch.lockDoor()
								self.entered_pin = ""
								self.keypad.lastKeyPressed = ""
							#If the user entered the incorrect pin
							else:
								self.lcd.setText("ACCESS DENIED", 2)
								self.database.logFailedAccess()
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
					self.lcd.setText("DOOR UNLOCKED", 1)
					self.entered_pin = ""
					self.keypad.lastKeyPressed = ""		

				#If the physical lock button is pressed
				if (Button.isLockButtonPressed() and (self.doorLatch.status == "UNLOCKED")):
					self.doorLatch.lockDoor()
					self.lcd.setText("DOOR LOCKED", 1)
					self.entered_pin = ""
					self.keypad.lastKeyPressed = ""	


				self.rfidReader.ser.flushInput()
				self.busy = False
				
				if (self.masterMode):
					self.lcd.setText('MASTER MODE')

				self.updateDoorStatusInApp()


if __name__ == '__main__':
	try:
		#Initialize the Lock System and start running
		lock = SmartDoorLockSystem()
		lock.main()

	finally:
		pass
		#lock.lcd.setText('')
		#lock.database.mydb.close()
		#GPIO.cleanup()
