#!/usr/bin/env python3

from scraperclasses import Feed
import argparse, sys

parser = argparse.ArgumentParser(description='Scrape RSS feeds to build corpora.')
parser.add_argument('feedlist', nargs='?', type=argparse.FileType('r'),
	default=sys.stdin, help='a file containing a list of rss feeds, separated by newlines')
parser.add_argument('-o', '--outdir', dest='outdir', default='corpus.ky',
	help='the directory to output the corpus to')

args = parser.parse_args()


urls = [];

if args.feedlist != None:
	#print(args.feedlist[0])
	for line in args.feedlist: #{
		urls.append(line);
	#}

	
	for url in urls: #{
		print ('+' , url);
		feed = Feed(url)
		for source in feed.get_sources():
			print(source)
			source.add_to_archive(args.outdir)


else:
	parser.print_help()
