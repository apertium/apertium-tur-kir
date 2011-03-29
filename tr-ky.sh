sed 's/ /\n/g' |\
hfst-lookup -O apertium $TRMORPH 2> /dev/null |\
apertium-tagger -g tr-ky.prob |\
lt-proc -b tr-ky.autobil.bin
