import RPi.GPIO as GPIO

#Define the GPIO pins which the unlock and lock buttons are wired to
UNLOCK_BUTTON = 18
LOCK_BUTTON = 23

class Button(object):
	""" Indoor Button System """

	@staticmethod
	def setup():
		""" Button System Constructor """
		
		#Setup the GPIO pins
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(UNLOCK_BUTTON,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(LOCK_BUTTON,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)		

	@staticmethod
	def isUnlockButtonPressed():
		"""
		Unlock the Door Latch

		Parameters
	    	----------
	    	None
		
		Returns
	    	-------
	    	None
		"""
		
		#If the button was pressed, return True
		if (GPIO.input(UNLOCK_BUTTON) == GPIO.HIGH):
			return True
		
	@staticmethod
	def isLockButtonPressed():
		"""
		Unlock the Door Latch

		Parameters
	    	----------
	    	None
		
		Returns
	    	-------
	    	None
		"""
		
		#If the button was pressed, return True
		if (GPIO.input(LOCK_BUTTON) == GPIO.HIGH):
			return True

