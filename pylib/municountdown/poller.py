import threading
import random
import time

import municountdown.muni as muni
import municountdown.bart as bart


class Poller(threading.Thread):
	lock = None
	
	muni_at = None
	bart_delay = None
	muni_delay = None
	
	fakemode = False
	

	def __init__(self, fakemode = False):
		super(Poller, self).__init__()
		self.lock = threading.Lock()
		self.muni_at = -1
		self.bart_delay = None
		self.fakemode = fakemode
	
	def run(self):
		while True:
			self.poll()
			time.sleep(45)

	def poll(self):
		print("Polling!")

		if self.fakemode:
			self.muni_at = int(time.time() + 60 * 11)
			self.bart_delay = True
			self.muni_delay = False
			return;

		countdown = muni.get_interval()
		self.muni_at = int(time.time()) + int(countdown)
		self.bart_delay = bart.get_bsa()

