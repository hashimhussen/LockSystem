from RFIDReader import RFIDReader
import time

class TestRFIDReader():
	def main(self):
		random_tagIDs = ['11696246', '12345','1234', '0001231', '111111111111', '0', 'abc123']
		rfid_reader = RFIDReader()
		for input in random_tagIDs:
			#rfid_reader.ser.setDTR(1)
			rfid_reader.ser.write(input)
			tagID = rfid_reader.grab_rfid_data()
			print('Input: ' + input + '     Extracted Tag ID: ' + tagID[0] + '\n') 
			if tagID[0] == random_tagIDs[0]:
				print('valid')
			time.sleep(10)


if __name__ == '__main__':
	test = TestRFIDReader()
	test.main()
