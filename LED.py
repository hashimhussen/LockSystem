import RPi.GPIO as GPIO

RED_LED = 14
GREEN_LED = 15

class LED(object):
	""" LED System """

	@staticmethod
	def setup():
		""" LED Constructor """
		
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(RED_LED,GPIO.OUT, initial=GPIO.HIGH)
		GPIO.setup(GREEN_LED,GPIO.OUT, initial=GPIO.LOW)		

	@staticmethod
	def updateLEDs(doorState):
		if (doorState == "LOCKED"):
			GPIO.output(RED_LED,GPIO.HIGH)
			GPIO.output(GREEN_LED,GPIO.LOW)

		elif (doorState == "UNLOCKED"):
			GPIO.output(RED_LED,GPIO.LOW)
			GPIO.output(GREEN_LED,GPIO.HIGH)

