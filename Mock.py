class Mock():
	class Keypad():
		def __init__(self):
			self.lastKeyPressed = ""

		def keyPressed(self,key):
			time.sleep(0.2)
			self.lastKeyPressed = key


	class RFIDReader:
		def grab_rfid_data(self):
			#return ('12345',)
			return ('5390790',)


	class LCD():
		def setText(self,message, displayTime=None):
			print(message + '\n')


	class DoorLatch():
		def unlockDoor(self):
			print('Door has been unlocked')
		def lockDoor(self):
			print('Door has been locked')