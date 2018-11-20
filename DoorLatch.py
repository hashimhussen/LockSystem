import time
import RPi.GPIO as GPIO

class DoorLatch(object):
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		DOORLATCH = 18 #TODO - randomly chosen pin for now
		GPIO.setup(DOORLATCH, GPIO.OUT)

	def unlockDoor(self):
		GPIO.output(DOORLATCH, True)

	def lockDoor(self):
		GPIO.output(DOORLATCH, False)
