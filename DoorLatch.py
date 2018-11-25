import time
import RPi.GPIO as GPIO

class DoorLatch(object):
	""" An Electromagnetic Door Latch """

	def __init__(self):
		""" Door Latch Constructor """

		#Set the GPIO mode
		GPIO.setmode(GPIO.BCM)
		
		#Set the latch GPIO number (BCM numbering)
		self.DOORLATCH = 14

		#Set the latch GPIO as an output
		GPIO.setup(self.DOORLATCH, GPIO.OUT)

		#Initialize GPIO pin as FALSE, to ensure the latch is locked
		GPIO.output(self.DOORLATCH, GPIO.LOW)

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

		#Set the latch GPIO pin to HIGH
		GPIO.output(self.DOORLATCH, GPIO.HIGH)

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

		#Set the latch GPIO pin to LOW
		GPIO.output(self.DOORLATCH, GPIO.LOW)


