import re
import lxml.html
import lxml.html.clean
from urllib import request
from hashlib import sha1

class Scraper(object):
	
	def __init__(self, url): #, content):
		self.url = url
		#self.content = content
		self.aid = self.url_to_aid(url)

	def get_content(self):
		self.content = request.urlopen(self.url).read().decode('utf-8')
		self.doc = lxml.html.fromstring(self.content)



class ScraperKloop(Scraper):
	domain = "kmb3.kloop.kg"
	prefix = "kloop"
	rePagenum = re.compile("p(|age)=([0-9]*)")
	badClasses = ['vk-button', 'mailru-button', 'fb-share-button', 'odkl-button', 'twitter-horizontal', 'live-journal', 'google-buzz', 'mrc__share']


	def scraped(self):
		self.get_content()
		#print(self.doc)
		for el in self.doc.find_class('entrytext'):
			pass
		#return lxml.html.document_fromstring(lxml.html.clean.clean_html(lxml.html.tostring(el).decode('utf-8'))).text_content()
		cleaned = lxml.html.document_fromstring(lxml.html.clean.clean_html(lxml.html.tostring(el).decode('utf-8')))
		for className in self.badClasses:
			for el in cleaned.find_class(className):
				el.getparent().remove(el)
		#remove all h3 tags
		for badEl in cleaned.findall(".//h3"):
			badEl.getparent().remove(badEl)

		return cleaned.text_content()

	def url_to_aid(self, url):
		return self.rePagenum.search(url).groups()[1]

class ScraperAzattyk(Scraper):
	domain = "www.azattyk.org"
	prefix = "rferl"

	def scraped(self):
		self.get_content()
		#print(self.doc)
		for el in self.doc.find_class('zoomMe'):
			pass
		cleaned = lxml.html.document_fromstring(lxml.html.clean.clean_html(lxml.html.tostring(el).decode('utf-8')))
		#for className in self.badClasses:
		#	for el in cleaned.find_class(className):
		#		el.getparent().remove(el)
		return cleaned.text_content()

	def url_to_aid(self, url):
		return sha1(url.encode('utf-8')).hexdigest()

class ScraperTRT(Scraper):
	domain = "www.trtkyrgyz.com"
	prefix = "trt"
	rePagecode = re.compile("haberkodu=([0-9a-f\-]*)(.html)?")

	def scraped(self):
		self.get_content()
		cleaned = lxml.html.document_fromstring(lxml.html.clean.clean_html(self.content))
		output = ""
		for el in cleaned.findall(".//p"):
			#for subel in el.getiterator():
			#	output += subel.text
			output += el.text_content()
			#print(el.text)
		return output

		#print(self.url)
	
	def url_to_aid(self, url):
		return self.rePagecode.search(url).groups()[0]

class ScraperBBC(Scraper):
	domain = "www.bbc.co.uk"
	prefix = "bbc"
	
	def scraped(self):
		self.get_content()
		el = None
		for el in self.doc.find_class('bodytext'):
			pass
		if el != None:
			cleaned = lxml.html.document_fromstring(lxml.html.clean.clean_html(lxml.html.tostring(el).decode('utf-8')))
			return cleaned.text_content()
		else:
			return False

	def url_to_aid(self, url):
		return sha1(url.encode('utf-8')).hexdigest()

class ScraperAlaman(Scraper):
	domain = "alamankg.org"
	prefix = "alaman"
	reArticleNum = re.compile("\/([0-9]*?)\/?$")
	reBadDomain = re.compile("^http://alaman\\.kg/(.*)")

	def __init__(self, url):
		# Alaman's rss feed points urls in a domain that forwards to the correct domain but without the content; this logic corrects the domain
		if self.reBadDomain.match(url):
			self.url = self.reBadDomain.sub('http://alamankg.org/\g<1>', url)
			print(">> "+self.url)
		else:
			self.url = url

		self.aid = self.url_to_aid(url)

	def scraped(self):
		self.get_content()
		el = None
		for el in self.doc.find_class('viewnew'):
			pass
		if el != None:
			cleaned = lxml.html.document_fromstring(lxml.html.clean.clean_html(lxml.html.tostring(el).decode('utf-8')))
			return cleaned.text_content()
		else:
			return False

	def url_to_aid(self, url):
		return self.reArticleNum.search(url).groups()[0]
