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
		"""
		Listen for incoming UDP messages

		Parameters
	    	----------
	    	None
		
		Returns
	    	-------
	    	None
		"""
		#Listen for incoming UDP messages and proces them accordingly using the enum defined in UDP.py
		while True:
			buf, address = self.socket.recvfrom(2048)
			if len(buf):
				UDP.processMessage(buf,self.doorLatch)

	def updateDoorStatusInApp(self):
		"""
		Send a UDP message of the current doorState to the app on every iteration

		Parameters
	    	----------
	    	None
		
		Returns
	    	-------
	    	None
		"""
		#Setup the target of the UDP messages and the send the current door state
		host = "192.168.43.1"
		port = 8888
		target_address = (host,port)
		data = self.doorLatch.status
		self.socket.sendto(data.encode('utf-8'), target_address)

	def main(self):
		#Create a new thread to always listen for UDP messages
		t = Thread(target=self.listen_for_messages)
		t.daemon = True
		t.start()
		
		#Infinite Loop
		while True:
			#
			# RFID LOGIC
			#
			if (self.busy != True): #self.busy variable is needed to prevent the logic loop from breaking
				#Scan for an RFID card every iteration
				tagID = self.rfidReader.grab_rfid_data()
				
				#If the tagID returned was nothing (no tag was scanned)
				if (tagID[0] != ""): #tagID is a tuple
					self.busy = True

					#If a master tag was scanned, switch between normal mode and master mode
					if (self.database.isMasterTag(tagID[0])):
						if (self.masterMode):
							self.lcd.setText('')
							self.masterMode = False
							time.sleep(1)
						else:
							self.lcd.setText('MASTER MODE')
							self.masterMode = True
							time.sleep(1)
					#If a normal tag was scanned
					else:
						#If in master mode
						if (self.masterMode):
							#Remove the tag from the database if found
							if (self.database.isTagInDatabase(tagID[0])):
								if (self.database.removeTagFromDatabase(tagID[0])):
									self.lcd.setText('TAG DEACTIVATED', 2)
								else:
									self.lcd.setText('FAILED TO \nDEACTIVATE TAG', 2)
							#Add the tag to the database if not found
							else:
								if (self.database.addTagToDatabase(tagID[0])):
									self.lcd.setText('TAG ACTIVATED', 2)
								else:
									self.lcd.setText('FAILED TO \nACTIVATE TAG', 2)
						#If in normal mode
						else:
							#If the tag is in the database, unlock the door
							if self.database.isTagInDatabase(tagID[0]):
								self.doorLatch.unlockDoor()
								self.lcd.setText('ACCESS GRANTED', 2)
								time.sleep(3)
								self.doorLatch.lockDoor()
							#If the tag is NOT in the database, log the failed entry
							else:
								self.lcd.setText('ACCESS DENIED', 2)
								self.database.logFailedAccess()
				#
				# KEYPAD LOGIC
				#
				
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
				
					#If the '*' key is pressed, submit the entered keycode
					if ((self.keypad.lastKeyPressed == '*')):	
						#If the entered pin is of the correct length
						if ((len(self.entered_pin)-1) == len(self.correct_pin)):	
							#If the user entered the correct pin
							if (self.entered_pin[:-1] == self.correct_pin):
								#Update the system state
								self.doorLatch.unlockDoor()
								self.lcd.setText("ACCESS GRANTED", 2)
								time.sleep(3)
								self.doorLatch.lockDoor()
								self.entered_pin = ""
								self.keypad.lastKeyPressed = ""
							#If the user entered the incorrect pin
							else:
								#Update the system state, and log the failed entry
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

				#If the physical unlock button is pressed, update the system state
				if (Button.isUnlockButtonPressed() and (self.doorLatch.status == "LOCKED")):
					self.doorLatch.unlockDoor()
					self.lcd.setText("DOOR UNLOCKED", 1)
					self.entered_pin = ""
					self.keypad.lastKeyPressed = ""		

				#If the physical lock button is pressed, update the system state
				if (Button.isLockButtonPressed() and (self.doorLatch.status == "UNLOCKED")):
					self.doorLatch.lockDoor()
					self.lcd.setText("DOOR LOCKED", 1)
					self.entered_pin = ""
					self.keypad.lastKeyPressed = ""	

				#Flush the serial input on every iteration, to prevent a tag from being read multiple times
				self.rfidReader.ser.flushInput()
				#Reset the busy state to False
				self.busy = False
				
				#If in master mode, clearly display that this is the case
				if (self.masterMode):
					self.lcd.setText('MASTER MODE')

				#Update the door status in app
				self.updateDoorStatusInApp()


if __name__ == '__main__':
	try:
		#Initialize the Lock System and start running
		lock = SmartDoorLockSystem()
		lock.main()

	finally:
		#Clean up
		lock.lcd.setText('')
		lock.database.mydb.close()
		GPIO.cleanup()
