#!/usr/bin/env python

import sys
sys.path.append("pylib")


#set up library
import municountdown.poller
import municountdown.writer

from LPD8806 import LPD8806


def main():
	p = municountdown.poller.Poller()
	p.start()


	w = municountdown.writer.Writer(p)
	w.start()



if __name__ == '__main__':
	main()
