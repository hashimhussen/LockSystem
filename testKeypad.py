import RPi.GPIO as GPIO
import time

class TestKeypad():
	KEYPAD = [
     	 		["1","2","3","A"],
		        ["4","5","6","B"],
		        ["7","8","9","C"], 
		        ["*","0","#","D"]
		 ]

	ROW_PINS = [2, 3, 4, 17]
	COL_PINS = [27, 22, 10, 9]
	DEFAULT_DEBOUNCE_TIME = 10

	GPIO.setmode(GPIO.BCM)

	def printKey(self):
		print(readKey() + 'was pressed')

	def readKey(self):
		# Set rows as input
		for i in range(len(ROW_PINS)):
	            GPIO.setup(ROW_PINS[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
	            GPIO.add_event_detect(ROW_PINS[i], GPIO.FALLING, callback=printKey, bouncetime=DEFAULT_DEBOUNCE_TIME)

	        # Set columns  as output
       		for j in range(len(COL_PINS)):
	            GPIO.setup(COL_PINS[j], GPIO.OUT)
        	    GPIO.output(COL_PINS[j], GPIO.LOW)


		# Scan pressed key row
		rowVal = None
		for i in range(len(ROW_PINS)):
			tmpRead = GPIO.input(ROW_PINS[i])
		        if tmpRead == 0:
	        		rowVal = i
	                	break

	        # Scan columns for pressed key
	        colVal = None
	        if rowVal is not None:
	            for i in range(len(COL_PINS)):
	                GPIO.output(COL_PINS[i], GPIO.HIGH)
	                if GPIO.input(COL_PINS[rowVal]) == GPIO.HIGH:
	                    GPIO.output(COL_PINS[i], GPIO.LOW)
	                    colVal = i
	                    break
	                GPIO.output(COL_PINS[i], GPIO.LOW)

	        # Find out the key that was pressed
	        if colVal is not None:
	            pressed_key = KEYPAD[rowVal][colVal]

	        return pressed_key

if __name__ == '__main__':
	keypad_test = TestKeypad()
	while (1):
		keypad_test.readKey()
	#GPIO.output(2, GPIO.HIGH)
	#GPIO.output(2, GPIO.LOW)
