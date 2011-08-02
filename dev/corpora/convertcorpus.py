#!/usr/bin/env python3

#import lxml.etree as etree
from lxml import etree
import os
import sys
from io import StringIO
from datetime import datetime
import re

if len(sys.argv) < 3:
	print("Usage: %s corpus_dir output_file" % sys.argv[0])
	sys.exit()

#output = open(sys.argv[2], 'w')
outfile = sys.argv[2]
os.chdir(sys.argv[1])
files = os.listdir('.')

##root = etree.parse(f).getroot()
##etree.SubElement(root, "entry", id="whatever").text = "TIS IS MY CONTENT"
##etree(root).write(f)
#root = etree.Element("corpus", xmlns="http://apertium.org/xml/corpus/0.9", language="ky", name="Kyrgyz News Corpus")

#tree = etree.parse(f)
#root = tree.getroot()

corpusNames = {
	"trt": "Kyrgyz TRT News Corpus",
	"history": "Kyrgyz Book Corpus",
	"bbc": "Kyrgyz BBC News Corpus",
	"kloop": "Kyrgyz kloop News Corpus",
	"rferl": "Kyrgyz RFERL News Corpus",
	"alaman": "Kyrgyz alaman News Corpus",
}

ids = {}

def populateIds(which, root):
	global ids
	if which not in ids:
		ids[which] = []
	
		for item in root.iter("{http://apertium.org/xml/corpus/0.9}entry"):
			ids[which] += [item.attrib['id']]

def idInTree(id, which):
	global ids
	#for item in root.iter("{http://apertium.org/xml/corpus/0.9}entry"):
	#	print(item.attrib['id'])
	#	if item.attrib['id'] == id:
	if id in ids[which]:
		print("already exists")
		return True
	return False

def addId(which, id):
	global ids
	ids[which] += [id]

def addToCorpus(which, id, title, timestamp, content, url=None):
	global corpusNames
	outfile = which + ".xml"

	if os.path.isfile(outfile):
		root = etree.parse(outfile).getroot()
	else:
		root = etree.Element("corpus", xmlns="http://apertium.org/xml/corpus/0.9", language="ky", name=corpusNames[which])
	populateIds(which, root)

	##source=which
	entry_id = source +"."+ id
	if not idInTree(entry_id, which):
		addId(which, entry_id)
		if url:
			etree.SubElement(root, "entry", source=url, id=entry_id, title=title, timestamp=outTime).text = content
		else:
			etree.SubElement(root, "entry", id=entry_id, title=title, timestamp=outTime).text = content

		etree.ElementTree(root).write(outfile, pretty_print=True, encoding='UTF-8', xml_declaration=False)
	
htmlFile = re.compile(".*\.html$")

for fn in files:
	if htmlFile.match(fn):
		(source, id, extension) = fn.split('.')
		stats = os.stat(fn)
		f = open(fn, 'r')
		#root = etree.fromstring("<html>"+open(f).read()+"</html>")
		inroot = etree.fromstring("<root>"+f.read()+"</root>")
		#newcontent = StringIO("<html>"+str(f.read())+"</html>")
		#root = etree.parse(newcontent).getroot()
		for item in inroot.getiterator("h1"):
			title = item.text.strip()
		#print(etree.tostring(root))
		url = None
		for item in inroot.getiterator("a"):
			url = item.attrib['href']
		for item in inroot.getiterator("div"):
			if item.attrib['class'] == 'content':
				content = item.text.strip() + '\n'
				break
		timeModified=stats.st_mtime
		#print(timeModified)
		outTime = datetime.fromtimestamp(timeModified).isoformat(' ')
		#print(outTime)
		#print(source, id, title)
		#if url:
		#	print(url)
	
		#print(fn)
		#f = open(fn, 'r')
		#x = False
		#for line in f:
		#	if line.strip() == '<div class="content">':
		#		x = True
		#	elif x == True:
		#		if line.strip() == "</div>":
		#		break
		#	elif line.strip() != ""
		#		output.write(line.strip() + "\n")
		#	f.close()
	
		##entry_id = element.attrib["source"] +"."+ element.attrib["id"]
		##source="bbc" id="f511447a"

		f.close()
		addToCorpus(source, id=id, title=title, timestamp=outTime, content=content, url=url)


#tree.write("corpus.ky.xml")
#root.write("corpus.ky.xml", encoding='utf-8')
print(len(files))
#etree.ElementTree(root).write(outfile, pretty_print=True, encoding='UTF-8', xml_declaration=False)
