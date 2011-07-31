#!/usr/bin/env python

#import xml.etree.ElementTree as etree
import os
import sys

if len(sys.argv) < 3:
	print("Usage: %s corpus_dir output_file" % sys.argv[0])
	sys.exit()

output = open(sys.argv[2], 'w')
os.chdir(sys.argv[1])
files = os.listdir('.')

for fn in files:
	print(fn)
	f = open(fn, 'r')
	x = False
	for line in f:
		if line.strip() == '<div class="content">':
			x = True
		elif x == True:
			if line.strip() == "</div>":
				break
			elif line.strip() != "":
				output.write(line.strip() + "\n")	
	f.close()
			

	#root = etree.parse(fn).getroot()
	#for item in root.getiterator("div"):
	#	if item.attrib['class'] == 'content':
	#		output.write(item.text.strip() + '\n')
	#		break

output.close()
print("Done.")
