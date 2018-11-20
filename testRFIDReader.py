from RFIDReader import RFIDReader
import time

class TestRFIDReader():
	def main(self):
		random_tagIDs = ['12345',1234, '0001231', '111111111111', 0, 'abc123']
		rfid_reader = RFIDReader()
		for input in random_tagIDs:
			rfid_reader.ser.setDTR(1)
			rfid_reader.ser.write(input)
			tagID = rfid_reader.grab_rfid_data()
			time.sleep(1)

			print('Input: ' + input + '     Extracted Tag ID: ' + tagID[0] + '\n') 

if __name__ == '__main__':
	test = TestRFIDReader()
	test.main()
