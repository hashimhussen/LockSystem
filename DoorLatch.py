from Adafruit_CharLCD import Adafruit_CharLCD
import time

class LCD(object):
	def __init__(self):
		# Setup LCD
		self.lcd = Adafruit_CharLCD(rs=12, en=5, d4=6, d5=13, d6=19, d7=26, cols=16, lines=2)
		self.lcd.clear()

	def setText(self,message,displayTime=None): #displayTime is how long the text will be displayed on the LCD
		self.lcd.clear()
		self.lcd.message(message)
		if displayTime != None: #If no displayTime is given, assume printing forever
			time.sleep(displayTime)
			self.lcd.clear()
