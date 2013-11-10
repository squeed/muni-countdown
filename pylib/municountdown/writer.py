#
# Handle writing to the actual sign
import sys
import threading
import time

import LPD8806.LPD8806 as LPD8806

TIMERLEN = 16 
STRIPLEN = TIMERLEN+4 # countdown timer + delay presence
RED = LPD8806.Color(200,50,50)
GREEN = LPD8806.Color(50, 200, 50)
YELLOW = LPD8806.Color(255, 150, 0)

class Writer(threading.Thread):
	
	poller = None
	stop = None
	strip = None

	def __init__(self, poller):
		super(Writer, self).__init__()
		self.poller = poller
		self.stop = False
		self.strip = LPD8806.LEDStrip(STRIPLEN)
		self.strip.setMasterBrightness(.5)

	
	"""Return the appropriate array of Colors corresponding
	to the present countdown time.
	The first 3 are red, then the next 5 green, then yellow.


	"""
	def timer_colors(self, minutes):
		
		if minutes > TIMERLEN:
			minutes = TIMERLEN

		if minutes < 0:
			return list();
		out = [LPD8806.Color(0, 0, 0)] * TIMERLEN

		for i in range(minutes):
			if i < 3:
				out[i] = RED
			elif i < 8:
				out[i] = GREEN
			else:
				out[i] = YELLOW

		return out

	def output(self):
		bartstr = "bart be okay"

		if self.poller.bart_delay:
			bartstr = "bart delay!"

		c = LPD8806.Color(255, 255, 0)

		seconds = self.poller.muni_at - time.time()
		minutes = round(seconds / 60 )
		if minutes > 0:
			self.strip.fillOff()
		
			self.strip[0:TIMERLEN] = self.timer_colors(minutes)

			if self.poller.bart_delay:
				self.strip[-3] =  RED
			else:
				self.strip[-3] =  GREEN

			self.strip.update()

		sys.stderr.write("There are {0} seconds {1} minutes 'till j. {2}\n".format(seconds, minutes, bartstr))



	def run(self):
		while True:
			self.output()
			time.sleep(10)


