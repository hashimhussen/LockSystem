import socket, time

from enum import Enum
from DoorLatch import DoorLatch


class Messages(Enum):
	#FOUND_IN_DATABASE = 1
	#NOT_FOUND_IN_DATABASE = 2
	UNLOCK_DOOR = 3
	LOCK_DOOR = 4
	GET_DOOR_STATUS = 5


class UDP(object):
	""" Collection of UDP related methods """

	@staticmethod
	def processMessage(message, doorLatch):
		print(message)
		print(Messages.UNLOCK_DOOR.value)
		if (int(message) == Messages.UNLOCK_DOOR.value):
			return doorLatch.unlockDoor()
		elif (int(message) == Messages.LOCK_DOOR.value):
			return doorLatch.lockDoor()
		elif (int(message) == Messages.GET_DOOR_STATUS.value):
			return doorLatch.status
		else:
			return "Invalid message type received"



