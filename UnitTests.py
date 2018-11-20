import unittest
import sqlite3
import serial
import time
from RFIDReader import RFIDReader

def connectToDatabase(path):
	return sqlite3.connect(path)

def serialConnectionExists():
	rfid_reader = RFIDReader()
	return rfid_reader

def serialOpen():
	rfid_reader = RFIDReader()
	return rfid_reader.ser.open()

def readTagID(tagID):
	rfid_reader = RFIDReader()
	rfid_reader.ser.write(tagID)
	#time.sleep(1)
	return rfid_reader.ser.readline()


class UnitTestCases(unittest.TestCase):
	def setUp(self):
		pass

	def test_databaseExists(self):
		self.assertIsNotNone(connectToDatabase('/home/pi/Desktop/allowedtags.db'))

	def test_databaseExists2(self):
		self.assertRaises(sqlite3.OperationalError, connectToDatabase, '/home/random/doesnotexist.db')

	def test_serialConnectionExists(self):
		self.assertIsNotNone(serialConnectionExists)

	def testSerialPortOpen(self):
		self.assertIsNotNone(serialOpen)

#	def test_readTagID1(self):
#		self.assertEqual(readTagID(b'12345'),('12345',))
	
#	def test_readTagID2(self):
#		self.assertRaises(TypeError, readTagID, 12345)


if __name__ == '__main__':
	unittest.main()
