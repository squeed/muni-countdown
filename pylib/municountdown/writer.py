#
# Handle writing to the actual sign
import threading
import time

class Writer(threading.Thread):
	
	poller = None
	stop = None

	def __init__(self, poller):
		super(Writer, self).__init__()
		self.poller = poller
		self.stop = False

	def output(self):
		bartstr = "bart be okay"

		if self.poller.bart_delay:
			bartstr = "bart delay!"

		print("There are {0} seconds 'till j. {1}".format(self.poller.seconds_to_j, bartstr))


	def run(self):
		while True:
			self.output()
			time.sleep(10)


