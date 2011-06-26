#!/usr/bin/env python3

import re, feedparser, urllib, os

class Scraper(object):

	content = None

	def __init__(self, content):
		self.content = content


class ScraperTRT(Scraper):

	replacements = [
		('<br /></strong>', '</strong><br />'),
		('<br />', '\n<br />\n'),
		('</p>', '\n</p>\n'),
		('</div>', '\n</div>\n'),
		('<p class="introduction">', '\n<p class="introduction">\n'),
		('<div class="author">', '\n<div class="author">\n'),
		('<div class="zoomMe">', '\n<div class="zoomMe">\n'),
		('<div class="date">', '\n<div class="date">\n')
	]

	sterilisation = [
		('&quot;', '"'),
		('&ldquo;', '“'),
		('&rdquo;', '”'),
		('&laquo;', '«'),
		('&raquo;', '»'),
		('&ndash;', '–'),
		('&mdash;', '—'),
		('&nbsp;', ' ')
	]


	def url_to_aid(url):
		return url.split('=')[1]
	
	def parse_html(self, s): #{
		for (patt, repl) in self.sterilisation:
			s = re.sub(patt, repl, s)
	
		return s;
	#}


	def scrape(self, content=None):
		if not content and self.content:
			content = self.content

		#global pageParser
		out = '';
		printing = False;

		for (subj, repl) in self.replacements:
			content = re.sub(subj, repl, content)
			#print(content)

		for line in content.split('\n'): #{
			if line.count('class="detay_aciklama">') > 0: #{
				printing = True;
			#}
			if line.count(' (www.trtkyrgyz.com)') > 0 or line.count('<div class="forum_comment_reply">') > 0: #{
				printing = False;
			#}

			if printing == True: #{
				out = out + self.parse_html(line) + '\n';
			#}
		#}

		return out;




class Feed(object):
	domain_name = re.compile('^http[s]{0,1}://(.*?)/.*')

	feed_sites = {
		"www.trtkyrgyz.com": ScraperTRT
	}

	which_scraper = None;
	feed = None;

	def __init__(self, url):
		self.which_scraper = self.get_scraper(url)
		self.feed = feedparser.parse(url);
		
		for item in self.feed["entries"]:
			for link in item["links"]:
				title = item["title"]
				print('++' , title);
				print('++' , item["link"]);
				Source(item["link"], scraper=self.which_scraper, title=title)
	
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
	url = None
	title = None
	scraper = None
	filename = None
	page_contents = None
	out_content = None

	def __init__(self, url, scraper=None, title=None):
		self.set_url(url)
		if not scraper:
			self.scraper = self.get_scraper(url)
		else: self.scraper = scraper
		if not self.scraper:
			raise Exception("No scraper set!")

		self.aid = self.scraper.url_to_aid(url)
		self.filename = "./articles/%s.html" % self.aid

		print(self.aid)

		if not self.filename_exists():
			self.page_contents = self.get_page(url)
			self.out_content = self.get_content()
			self.add_to_archive()
		else:
			print(self.filename, " exists!")


	def get_scraper(self, url):
		return
	
	def get_page(self, link):
		f = urllib.request.urlopen(link)
		return f.read().decode('utf-8')

	def get_content(self, contents=None):
		if not contents and self.page_contents:
			contents = self.page_contents
		scraper = self.scraper(contents)
		return scraper.scrape()

	def set_url(self, url):
		self.url = url
	
	def filename_exists(self):
		return os.path.isfile(self.filename)
	
	def add_to_archive(self):
		f = open(self.filename, 'w+');
		f.write('\n<div class="title">\n');
		f.write('<h1>' + str(self.title) + '</h1>\n');
		f.write('\n</div>\n');
		f.write(self.out_content);
		f.close();
