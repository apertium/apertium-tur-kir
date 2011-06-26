#!/usr/bin/python

import sys, codecs, copy, os, re;
import feedparser;
import urllib;

cur_title = '';
contents = '';
sterilisation = [('&quot;', '"'),
	('&ldquo;', '“'),
	('&rdquo;', '”'),
	('&laquo;', '«'),
	('&raquo;', '»'),
	('&ndash;', '–'),
	('&mdash;', '—'),
	('&nbsp;', ' ')]

pageParser = {}
pageParser["trt"] = [
	('<br /></strong>', '</strong><br />'),
	('<br />', '\n<br />\n'),
	('</p>', '\n</p>\n'),
	('</div>', '\n</div>\n'),
	('<p class="introduction">', '\n<p class="introduction">\n'),
	('<div class="author">', '\n<div class="author">\n'),
	('<div class="zoomMe">', '\n<div class="zoomMe">\n'),
	('<div class="date">', '\n<div class="date">\n')]

def read_page(buf): #{
	global contents;

	contents = contents + buf;
#}

def parse_html(s): #{
	global sterilisation
	for (subj, repl) in sterilisation:
		s = re.sub(subj, repl, s)
	#s = s.replace('&quot;', '"');
	#s = s.replace('&ldquo;', '“');
	#s = s.replace('&rdquo;', '”');
	#s = s.replace('&laquo;', '«');
	#s = s.replace('&raquo;', '»');
	#s = s.replace('&ndash;', '–');
	#s = s.replace('&mdash;', '—');
	#s = s.replace('&nbsp;', ' ');
	
	return s;
#}

def parse_page(buf): #{
	global pageParser
	out = '';
	printing = False;

	for (subj, repl) in pageParser["trt"]:
		buf = re.sub(subj, repl, buf)
		print(buf)
	#buf = buf.replace('<br /></strong>', '</strong><br />');
	#buf = buf.replace('<br />', '\n<br />\n');
	#buf = buf.replace('</p>', '\n</p>\n');
	#buf = buf.replace('</div>', '\n</div>\n');
	#buf = buf.replace('<p class="introduction">', '\n<p class="introduction">\n');
	#buf = buf.replace('<div class="author">', '\n<div class="author">\n');
	#buf = buf.replace('<div class="zoomMe">', '\n<div class="zoomMe">\n');
	#buf = buf.replace('<div class="date">', '\n<div class="date">\n');

	for line in buf.split('\n'): #{
		if line.count('class="detay_aciklama">') > 0: #{
			printing = True;
		#}
		if line.count(' (www.trtkyrgyz.com)') > 0 or line.count('<div class="forum_comment_reply">') > 0: #{
			printing = False;
		#}

		if printing == True: #{
			out = out + parse_html(line) + '\n';
		#}
	#}

	return out;
#}

urls = [];

for line in open('kyscraper_rss.dat').read().split('\n'): #{
	urls.append(line);
#}
	
for url in urls: #{
	print ('+' , url);
	feed = feedparser.parse(url);
	
	for item in feed["entries"]: #{
		contents = '';
		aid = '';
		for link in item["links"]:
			print('++' , link["href"]);
			aid = link["href"].split('=')[1];
			print(aid);
			#filename = str('./articles/' + aid + '.html');
			filename = "./articles/%s.html" % aid
	
			if aid == '' and contents == '': #{
				continue;
			#}
		
			if filename.count('?') > 0: #{
				continue;
			#}
		
			if os.path.isfile(filename): #{
				print(filename , ' file exists.');
				continue;
			#}
	
			cur_title = item["title"];
			print('++' , cur_title);
	
			print('++' , item["link"]);

			f = urllib.request.urlopen(item["link"])
			contents = f.read()
	
			content = parse_page(contents.decode('utf-8'));
	
			f = open(filename, 'w+');
			f.write('\n<div class="title">\n');
			f.write('<h1>' + cur_title + '</h1>\n');
			f.write('\n</div>\n');
			f.write(content);
			f.close();
		#}
	#}
#}

