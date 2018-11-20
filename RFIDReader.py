
#!/usr/bin/python

import serial, string, time

class RFIDReader:
	def __init__(self):
		self.ser = serial.Serial('/dev/ttyACM0', 9600,timeout = 0.2)
		self.status = 1 # 1 for open, 0 for closed

	def grab_rfid_data(self):
		return (self.ser.readline(),)
