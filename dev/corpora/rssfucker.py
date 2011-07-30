#!/usr/bin/env python
import xml.etree.ElementTree as etree
try: import urllib.request as urllib # py3
except: import urllib # py2

def parse_rss(url):
	rss = etree.parse(urllib.urlopen(url))
	out = {}
	for item in rss.getiterator("item"):
		out[item.find("title").text] = item.find("link").text
	return out

if __name__ == "__main__":
	import sys
	if len(sys.argv) > 1:
		for k, v in parse_rss(sys.argv[1]).items():
			print("%s: %s" % (k, v))
	else:
		print("Usage: %s url" % sys.argv[0])

