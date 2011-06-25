#!/usr/bin/python
# coding=utf-8
# -*- encoding: utf-8 -*-

import sys, codecs, copy, os;
import feedparser;
import pycurl;

sys.stdin  = codecs.getreader('utf-8')(sys.stdin);
sys.stdout = codecs.getwriter('utf-8')(sys.stdout);
sys.stderr = codecs.getwriter('utf-8')(sys.stderr);

cur_title = '';
contents = '';

def read_page(buf): #{
	global contents;

	contents = contents + buf;
#}

def parse_html(s): #{
	s = s.replace('&quot;', '"');
	s = s.replace('&ldquo;', '“');
	s = s.replace('&rdquo;', '”');
	s = s.replace('&laquo;', '«');
	s = s.replace('&raquo;', '»');
	s = s.replace('&ndash;', '–');
	s = s.replace('&mdash;', '—');
	s = s.replace('&nbsp;', ' ');
	
	return s;
#}

def parse_page(buf): #{
	out = '';
	printing = False;

	buf = buf.replace('<br /></strong>', '</strong><br />');
	buf = buf.replace('<br />', '\n<br />\n');
	buf = buf.replace('</p>', '\n</p>\n');
	buf = buf.replace('</div>', '\n</div>\n');
	buf = buf.replace('<p class="introduction">', '\n<p class="introduction">\n');
	buf = buf.replace('<div class="author">', '\n<div class="author">\n');
	buf = buf.replace('<div class="zoomMe">', '\n<div class="zoomMe">\n');
	buf = buf.replace('<div class="date">', '\n<div class="date">\n');

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

for line in file('kyscraper_rss.dat').read().split('\n'): #{
	urls.append(line);
#}
	
for url in urls: #{
	print '+' , url;
	feed = feedparser.parse(url);
	
	for item in feed["entries"]: #{
		contents = '';
		aid = '';
		for link in item["links"]:
			print '++' , link["href"] ;
			aid = link["href"].split('=')[1];
			print aid;
			filename = str('./articles/' + aid + '.html');
	
			if aid == '' and contents == '': #{
				continue;
			#}
		
			if filename.count('?') > 0: #{
				continue;
			#}
		
			if os.path.isfile(filename): #{
				print filename , ' file exists.';
				continue;
			#}
	
			cur_title = item["title"];
			print '++' , cur_title;
	
			print '++' , item["link"];
	
			c = pycurl.Curl();
			c.setopt(c.URL, str(item["link"]));
			c.setopt(c.WRITEFUNCTION, read_page);
			c.perform();
			c.close();
	
			content = parse_page(contents);
	
			f = file(filename, 'w+');
			f.write('\n<div class="title">\n');
			f.write('<h1>' + cur_title + '</h2>\n');
			f.write('\n</div>\n');
			f.write(content);
			f.close();
		#}
	#}
#}

