#!/usr/bin/env python3

from scraperclasses import Feed

urls = [];

for line in open('kyscraper_rss.dat').read().split('\n'): #{
	urls.append(line);
#}
	
for url in urls: #{
	print ('+' , url);
	feed = Feed(url)
