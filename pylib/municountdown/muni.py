#!/usr/bin/env python3.2

import urllib.request
import urllib.parse

import sys

import xml.etree.ElementTree


URL = 'http://webservices.nextbus.com/service/publicXMLFeed'
STOP = 13998

AGENCY = 'sf-muni'

def do_command(cmd, **args):
	args['a'] = 'sf-muni'
	args['command'] = cmd

	uu = URL + '?' + urllib.parse.urlencode(args)
	res = urllib.request.urlopen(uu)
	data = xml.etree.ElementTree.parse(res)

	if data is None:
		raise Exception("Polling error")

	
	return data
	


def get_interval(stopId = STOP):
	d = do_command('predictions', stopId= stopId)

	d = d.find('predictions')
	d = d.find('direction')
	xml.etree.ElementTree.dump(d)
	d = d.find('prediction')
	seconds =  int(d.get('seconds'))
	has_delay = 0
	if d.get("delayed") == "true":
		has_delay = 2
	elif d.get("affectedByLayover") == "true":
		has_delay = 1

	return (seconds, has_delay)

