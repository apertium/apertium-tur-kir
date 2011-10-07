#!/usr/bin/env python3
# punktgen.py

import sys, pickle
from nltk.tokenize import punkt

if len(sys.argv) < 3:
	print("Usage: %s infile outfile" % sys.argv[0])
	sys.exit()

tk = punkt.PunktSentenceTokenizer()
inf = open(sys.argv[1])
outf = open(sys.argv[2], 'wb')

tk.train(inf.read())
pickle.dump(tk, outf)

outf.close()
inf.close()
print(sys.argv[2] + " saved.")
