import RPi.GPIO as GPIO

UNLOCK_BUTTON = 18
LOCK_BUTTON = 23

class Button(object):
	""" Indoor Button System """

	@staticmethod
	def setup():
		""" Button System Constructor """
		
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(UNLOCK_BUTTON,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(LOCK_BUTTON,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)		

	@staticmethod
	def isUnlockButtonPressed():
		if (GPIO.input(UNLOCK_BUTTON) == GPIO.HIGH):
			return True
		
	@staticmethod
	def isLockButtonPressed():
		if (GPIO.input(LOCK_BUTTON) == GPIO.HIGH):
			return True

