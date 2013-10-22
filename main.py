#!/usr/bin/env python3

import sys
sys.path.append("pylib")

import time

#set up library
import municountdown.poller
import municountdown.writer


def main():
	p = municountdown.poller.Poller( False)
	p.start()
	time.sleep(5)


	w = municountdown.writer.Writer(p)
	w.start()



if __name__ == '__main__':
	main()
