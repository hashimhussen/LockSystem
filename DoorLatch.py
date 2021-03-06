import time, serial
import RPi.GPIO as GPIO
from LED import LED
from Button import Button

UNLOCK = 0
LOCK = 1

class DoorLatch(object):
	""" An Electromagnetic Door Latch """

	def __init__(self):
		""" Door Latch Constructor """

		#Open a serial connection to the Arduino
		self.ser = serial.Serial('/dev/ttyACM0', 9600,timeout = 0.2)

		self.status = "LOCKED"

		#Initialize the LED System
		LED.setup()

		#Initialize the hardware buttons
		Button.setup()

	def unlockDoor(self):
		"""
		Set the latch pin state to HIGH, retracting the latch (a.k.a. unlocking door)

		Parameters
	    	----------
	    	None

		Returns
	    	-------
	    	None
		"""

		#Unlock the door
		self.ser.write("%d"%UNLOCK)

		#Update the door status
		self.status = "UNLOCKED"

		#Update the LEDs
		LED.updateLEDs(self.status)

	def lockDoor(self):
		"""
		Set the latch pin state to HIGH, retracting the latch (a.k.a. unlocking door)

		Parameters
	    	----------
	    	None

		Returns
	    	-------
	    	None
		"""

		#Lock the door
		self.ser.write("%d"%LOCK)

		#Update the door status
		self.status = "LOCKED"

		#Update the LEDs
		LED.updateLEDs(self.status)



