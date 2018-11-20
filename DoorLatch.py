import time
import RPi.GPIO as GPIO

class DoorLatch(object):
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		self.DOORLATCH = 14 #TODO - randomly chosen pin for now
		GPIO.setup(self.DOORLATCH, GPIO.OUT)
		GPIO.output(self.DOORLATCH, False)

	def unlockDoor(self):
		GPIO.output(self.DOORLATCH, True)

	def lockDoor(self):
		GPIO.output(self.DOORLATCH, False)
