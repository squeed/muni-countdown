#
# Handle writing to the actual sign
import sys
import threading
import time
from datetime import datetime
from dateutil import tz

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
	timezone = None

	def __init__(self, poller):
		super(Writer, self).__init__()
		self.poller = poller
		self.stop = False
		self.strip = LPD8806.LEDStrip(STRIPLEN)
		self.strip.setMasterBrightness(.5)
		timezone = tz.gettz('America/Los_Angeles')
	
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

	def display_time(self):

		status_str = ""
		c = LPD8806.Color(255, 255, 0)

		seconds = self.poller.muni_at - time.time()
		minutes = round(seconds / 60 )
		if minutes > 0:
			self.strip.fillOff()
		
			self.strip[0:TIMERLEN] = self.timer_colors(minutes)

			if self.poller.bart_delay:
				status_str = "bart delay!"
				self.strip[-3] =  RED
			else:
				status_str = "bart ok"
				self.strip[-3] =  GREEN

			if self.poller.muni_delay == 2:
				status_str = status_str + " muni delay"
				self.strip[-1] = RED
			elif self.poller.muni_delay == 1:
				status_str = status_str + " muni star"
				self.strip[-1] = YELLOW
			else:
				status_str = status_str + " muni OK"
				self.strip[-1] = GREEN

			self.strip.update()

		sys.stderr.write("There are {0} seconds {1} minutes 'till j. {2}\n".format(seconds, minutes, status_str))

	def display_off(self):
		self.strip.all_off()


	def output(self):
		#get the time of day; display countdown between 0800 - 2200 local
		now = datetime.now(tz=self.timezone)
		if (now.hour > 8 and now.hour < 22):
			self.display_time()
		else:
			self.display_off()
		
	def run(self):
		while True:
			self.output()
			time.sleep(10)


