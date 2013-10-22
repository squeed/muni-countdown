#
# Handle writing to the actual sign
import threading
import time

import LPD8806.LPD8806 as LPD8806

TIMERLEN = 12
STRIPLEN = TIMERLEN+4 # countdown timer + delay presence

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
		red_c = LPD8806.Color(200,50,50)
		green_c = LPD8806.Color(50, 200, 50)
		yell_c = LPD8806.Color(255, 150, 0)

		if minutes >= TIMERLEN:
			minutes = TIMERLEN
		out = list()
		for i in range(minutes):
			if i < 3:
				out.append(red_c)
			elif i < 8:
				out.append(green_c)
			else:
				out.append(yell_c)

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
		
			self.strip[0:minutes] = self.timer_colors(minutes)

			if self.poller.bart_delay:
				self.strip[-1] = LPD8806.Color(255, 0, 0)

			self.strip.update()

		print("There are {0} seconds {1} minutes 'till j. {2}".format(seconds, minutes, bartstr))



	def run(self):
		while True:
			self.output()
			time.sleep(10)


