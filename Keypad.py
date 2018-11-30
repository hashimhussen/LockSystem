from pad4pi import rpi_gpio
import time

class Keypad(object):
	""" A 4x4 Matrix Keypad """

	def __init__(self):
		"""Keypad Constructor"""

		# Setup Keypad Layout
		KEYPAD = [
		        ["1","2","3","A"],
		        ["4","5","6","B"],
		        ["7","8","9","C"],
		        ["*","0","#","D"]
		]
		#Pi BCM Pins used 
		ROW_PINS = [2, 3, 4, 17]
		COL_PINS = [27, 22, 10, 9]

		self.lastKeyPressed = ""

		#Keypad initialization code
		self.factory = rpi_gpio.KeypadFactory()
		self.keypad = self.factory.create_keypad(keypad=KEYPAD, 
                                                         row_pins=ROW_PINS,
                                                         col_pins=COL_PINS)
		

		#keyPressed will be called each time a keypad button is pressed
		self.keypad.registerKeyPressHandler(self.keyPressed)

	def keyPressed(self,key):
		"""
		Set lastKeyPressed as the last key pressed on the Keypad
    		This will allow us to always have access to the last key pressed

		Parameters
	    	----------
	    	key : string
			Global variable set by the interrupt
			Stores the last key pressed on the Keypad

		Returns
	    	-------
	    	None
		"""

		time.sleep(0.2)
		self.lastKeyPressed = key

