from html.parser import HTMLParser
from hashlib import sha1
import re
import lxml.html

class HTMLParserSimple(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.title = ""
		self.is_title = False
		self.content = ""
		self.is_content = False

	def handle_starttag(self, tag, attrs):
		if tag == 'title':
			self.is_title = True
		if tag == 'p':
			self.is_content = True

	def handle_data(self, data):
		if self.is_title:
			self.title = data
			self.is_title = False
		if self.is_content:
			self.content += "\n" + data
			self.is_content = False

	def get_pages(self):
		return (self.title, self.content)

class HTMLParserAzattyk(HTMLParser):
	domain = "www.azattyk.org"
	prefix = "rferl"
	count = -1
	tagname = None

	def __init__(self):
		HTMLParser.__init__(self)
		self.content = ""
		self.is_content = False
		self.other_content = False
		self.skip = False

	def handle_starttag(self, tag, attrs):
		for (attr, value) in attrs:
			if self.count < 0 and attr == 'class' and value == 'zoomMe':
				self.tagname = tag
			elif attr == 'class' and value == 'photo_caption':
				self.other_content = True
		if tag == self.tagname:
			self.count += 1
		if tag == "script":
			self.skip = True

	def handle_endtag(self, tag):
		if tag == "script":
			self.skip = False
		if tag == self.tagname:
			self.count -= 1
			if self.count == -1:
				self.tagname = None

	def handle_data(self, data):
		if self.count >= 0 and not self.skip:
			self.content += data

		if self.other_content:
			self.content += "\n" + data + "\n"
			self.other_content = False

	def get_content(self):
		return self.content

	def url_to_aid(self, url):
		return sha1(url.encode('utf-8')).hexdigest()

class HTMLParserKloop(HTMLParser):
	domain = "kmb3.kloop.kg"
	prefix = "kloop"
	count = -1
	tagname = None
	rePagenum = re.compile("p(|age)=([0-9]*)")

	def __init__(self):
		HTMLParser.__init__(self)
		self.content = ""
		self.is_content = False
		self.other_content = False
		self.skip = False

	def handle_starttag(self, tag, attrs):
		for (attr, value) in attrs:
			if self.count < 0 and attr == 'class' and value == '':
				self.tagname = tag
			#elif attr == 'class' and value == 'photo_caption':
			#	self.other_content = True
		if tag == self.tagname:
			self.count += 1
		if tag == "script":
			self.skip = True

	def handle_endtag(self, tag):
		if tag == "script":
			self.skip = False
		if tag == self.tagname:
			self.count -= 1
			if self.count == -1:
				self.tagname = None

	def handle_data(self, data):
		if self.count >= 0 and not self.skip:
			self.content += data

		#if self.other_content:
		#	self.content += "\n" + data + "\n"
		#	self.other_content = False

	def get_content(self):
		return self.content

	def url_to_aid(self, url):
		return self.rePagenum.search(url).groups()[1]
		#return sha1(url.encode('utf-8')).hexdigest()

