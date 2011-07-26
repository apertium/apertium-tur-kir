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
		content = request.urlopen(self.url).read().decode('utf-8')
		self.doc = lxml.html.fromstring(content)



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
		badEl = cleaned.find(".//h3")
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
