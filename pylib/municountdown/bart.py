#!/usr/bin/env python3

import urllib.request
import urllib.parse

import sys

import xml.etree.ElementTree

URL = 'http://api.bart.gov/api/bsa.aspx'
KEY = 'MW9S-E7SL-26DU-VV8V'


def do_command(cmd, **args):
	args['cmd'] = cmd
	args['key'] = KEY
	
	uu = URL + '?' + urllib.parse.urlencode(args)

	res = urllib.request.urlopen(uu)
	data = xml.etree.ElementTree.parse(res)
	return data

def get_bsa():
	d = do_command('bsa')

	if d.find('bsa'):
		print("Delay found...")
		return True
	else:
		print("No Delay!")
		return False
