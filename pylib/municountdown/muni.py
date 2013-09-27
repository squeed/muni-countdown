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
	
	return data
	


def get_interval(stopId):
	d = do_command('predictions', stopId= stopId)

	#f = open('stop.xml')
	#d = xml.etree.ElementTree.parse(f)
	d = d.find('predictions')
	d = d.find('direction')
	d = d.find('prediction')
	return d.get('seconds')





#do_command('routeConfig', r='J')

print(get_interval(STOP))
