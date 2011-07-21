from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
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
			self.content += data
			self.is_content = False

	def get_pages(self):
		return (self.title, self.content)
