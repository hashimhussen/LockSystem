import serial, string, time

class RFIDReader:
	""" An RFID Reader """

	def __init__(self):
		""" RFID Reader Constructor """

		#Open a serial connection to the Arduino
		self.ser = serial.Serial('/dev/ttyACM0', 9600,timeout = 0.2)

	def grab_rfid_data(self):
		"""
		Retrieve the RFID Tag ID from over the serial connection to the Arduino

		Parameters
	    	----------
	    	None

		Returns
	    	-------
	    	(self.ser.readline(),) : tuple
				       A tuple containing the tagID read over the serial port
		"""

		# Returns the tagID as a tuple
		# *** Tag IDs are output onto the serial port after a tag is scanned 
		# the reader and the Arduino e.g. "513455\n" ***
		return (self.ser.readline(),)
