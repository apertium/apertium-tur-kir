#!/usr/bin/env python3

import re, feedparser, urllib, os
from bottle import template
from hashlib import sha1
#from html_parser import MyHTMLParser
#from scraper_parsers import *
from scrapers import *


class Feed(object):

	domain_name = re.compile('^http[s]{0,1}://(.*?)/.*')

	feed_sites = {
		#"www.trtkyrgyz.com": ScraperTRT,
		##"www.azattyk.org": ScraperAzattyk,
		#"www.azattyk.org": HTMLParserAzattyk,
		##"kmb3.kloop.kg": ScraperKMB
		##"kmb3.kloop.kg": HTMLParserKloop
		"kmb3.kloop.kg": ScraperKloop
	}

	which_scraper = None;
	feed = None;

	def __init__(self, url):
		self.which_scraper = self.get_scraper(url)
		self.feed = feedparser.parse(url)
		#print(self.feed)
		
	def get_sources(self):
		for item in self.feed["entries"]:
			for link in item["links"]:
				title = item["title"]
				print('++' , title);
				print('++' , item["link"]);
				thisScraper = self.which_scraper
				yield Source(item["link"], scraper=thisScraper, title=title)
	
	def get_scraper(self, url):
		domain = self.domain_name.match(url).group(1)
		which_scraper = self.feed_sites.get(domain)
		if which_scraper == None:
			raise Exception("Can't get scraper!")
		else:
			return which_scraper
		#else: Feed(url, which_scraper)


class Source(object):
	aid = None
	#url = None
	#title = None
	scraper = None
	parser = None
	filename = None
	page_contents = None
	out_content = None

	def __init__(self, url, scraper=None, title=None):
		#self.set_url(url)
		self.url = url
		self.title = title
		#self.outdir = outdir
		if not scraper:
			self.scraper = self.get_scraper(url)
		else: self.scraper = scraper
		if not self.scraper:
			raise Exception("No scraper set!")
		#self.page_contents = self.get_page(self.url)

		#print(self.scraper)
		#self.aid = self.scraper.url_to_aid(url)
		#self.filename = self.scraper.prefix+".%s.html" % self.aid
		#self.parser = self.scraper

		print(self.aid)

	def get_scraper(self, url):
		return
	
	def get_page(self, link):
		f = urllib.request.urlopen(link)
		return f.read().decode('utf-8')

	#def get_content(self, contents=None):
	#	if not contents and self.page_contents:
	#		contents = self.page_contents
	#	scraper = self.scraper(contents)
	#	return scraper.scrape()

	#def set_url(self, url):
	#	self.url = url
	
	def filename_exists(self):
		return os.path.isfile(self.path)
	
	def add_to_archive(self, outdir):
		scraper = self.scraper(self.url) #, self.page_contents)
		self.aid = scraper.aid
		self.filename = self.scraper.prefix+".%s.html" % self.aid

		self.outdir = outdir
		self.path = os.path.join(self.outdir, self.filename)
		if not self.filename_exists():
			#self.page_contents = self.get_page(self.url)
			#self.out_content = self.get_content()
			#parser = self.parser
			#print(self.page_contents.split('\n')[914])
			#try:
			#	parser.feed(self.page_contents)
			#except Exception:
			#	pass
			#self.out_content = parser.get_content()
			self.out_content = scraper.scraped()

			#print(outdir, self.filename, self)
			#with open(os.path.join(outdir, self.filename), 'w+') as f:
			with open(os.path.join(self.path), 'w+') as f:
			#f = open(os.path.join(outdir, self.filename), 'w+');
				f.write(template('source', title=self.title, content=self.out_content, url = self.url))
				#f.write('\n<div class="title">\n');
				#f.write('<h1>' + str(self.title) + '</h1>\n');
				#f.write('\n</div>\n');
				#f.write(self.out_content);
			#f.close();

		else:
			print(self.filename, " exists!  Skipping.")


class SimpleHtmlScraper(object):
	def url_to_aid(self, url):
		return sha1(url.encode('utf-8')).hexdigest()

	def __init__(self, prefix, url, outdir):
		self.url = url
		self.prefix = prefix
		self.outdir = outdir
		self.aid = self.url_to_aid(url)
		#self.filename = self.prefix+".%s.html" % self.aid
		self.filename = "%s.%s.html" % (self.prefix, self.aid)
		self.title = ""
		self.content = ""
		self.path = os.path.join(self.outdir, self.filename)
	
	def write(self):
		if self.url_not_in_path():
			with open(self.path, 'w+') as f:
				f.write(template('source', title=self.title, content=self.content, url = self.url))
	
	def parse(self):
		if self.url_not_in_path():
			content = urllib.request.urlopen(self.url)
			page = content.read().decode('utf-8')
			#myparser = MyHTMLParser()
			myparser = HTMLParserSimple()
			myparser.feed(page)
			(self.title, self.content) = myparser.get_pages()

	def url_not_in_path(self):
		return not os.access(self.path, os.F_OK)
