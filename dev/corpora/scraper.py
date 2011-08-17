#!/usr/bin/env python3

from scraper_classes import Feed, SimpleHtmlScraper
import argparse, sys
import urllib.error
import socket


parser = argparse.ArgumentParser(description='Scrape RSS feeds to build corpora.')
parser.add_argument('feedlist', nargs='?', type=argparse.FileType('r'),
	default=sys.stdin, help='a file containing a list of rss feeds, separated by newlines')
parser.add_argument('-o', '--outdir', dest='outdir', default='corpus.ky',
	help='the directory to output the corpus to')
parser.add_argument('-r', '--rss', dest='read_as_rss', default=True, help='whether or not to assume source is rss')

args = parser.parse_args()

urls = [];

if args.feedlist != None:
	#print(args.feedlist[0])
	for line in args.feedlist: #{
		urls.append(line);
	#}

	
	for url in urls: #{
		print ('+' , url);
		if bool(int(args.read_as_rss)):
			feed = Feed(url)
			#print(feed.feed)
			for source in feed.get_sources():
				#print(source)
				try:
					source.makeRoot(args.outdir)
					source.add_to_archive()
				except urllib.error.HTTPError:
					print("*** "+str(urllib.error.HTTPError))
				except urllib.error.URLError:
					print("*** "+str(urllib.error.URLError))
				except socket.gaierror:
					print("*** "+str(socket.gaierror))

		else:
			page = SimpleHtmlScraper("history", url, args.outdir)
			page.parse()
			page.write()


else:
	parser.print_help()
