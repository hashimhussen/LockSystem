from Adafruit_CharLCD import Adafruit_CharLCD
import time

class LCD(object):
	""" A 16x2 LCD Display """

	def __init__(self):
		""" LCD Constructor """
		

		# Setup LCD
		self.lcd = Adafruit_CharLCD(rs=12, en=5, d4=6, 	 # Pins are being hardcoded
                                            d5=13, d6=19, d7=26, # 
                                            cols=16, lines=2)	 # (16x2 LCD)
		# Clear the LCD
		self.lcd.clear()


	def setText(self,message,displayTime=None):
		"""
		Set the LCD display text

		Parameters
	    	----------
	    	message : string
		        The message to be displayed on the LCD

	    	displayTime : int,optional
		            The amount of time the message will be displayed
			    If omitted, the message will disappear once the LCD is cleared

		Returns
	    	-------
	    	None
		"""

		# Clear the LCD
		self.lcd.clear()

		# Set the LCD text
		self.lcd.message(message)

		#If displayTime is provided, sleep for 'displayTime' seconds, then clear LCD
		if displayTime != None: 
			time.sleep(displayTime)
			self.lcd.clear()




