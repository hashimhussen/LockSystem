import RPi.GPIO as GPIO

#GPIO pins used for LEDs
RED_LED = 14
GREEN_LED = 15

class LED(object):
	""" LED System """

	@staticmethod
	def setup():
		""" LED Constructor """
		
		#Setup the GPIO pins
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(RED_LED,GPIO.OUT, initial=GPIO.HIGH)
		GPIO.setup(GREEN_LED,GPIO.OUT, initial=GPIO.LOW)		

	@staticmethod
	def updateLEDs(doorState):
		"""
		Update the state of the LEDs according to the door state

		Parameters
	    	----------
	    	doorState : string
		        The current state of the door

		Returns
	    	-------
	    	None
		"""
		#If the door is currently locked
		if (doorState == "LOCKED"):
			#Update the LEDs
			GPIO.output(RED_LED,GPIO.HIGH)
			GPIO.output(GREEN_LED,GPIO.LOW)
		
		#If the door is currently unlocked
		elif (doorState == "UNLOCKED"):
			#Update the LEDs
			GPIO.output(RED_LED,GPIO.LOW)
			GPIO.output(GREEN_LED,GPIO.HIGH)

