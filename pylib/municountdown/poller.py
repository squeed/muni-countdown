import threading
import random
import time


class Poller(threading.Thread):
	lock = None
	
	seconds_to_j = None
	bart_delay = None
	

	def __init__(self):
		super(Poller, self).__init__()
		self.lock = threading.Lock()
		self.seconds_to_j = -1
		self.bart_delay = None
	
	def run(self):
		while True:
			self.poll()
			time.sleep(45)

	def poll(self):
		print("Polling!")

		self.seconds_to_j = random.randint(0, 999)
		self.bart_delay = True

