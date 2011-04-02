all:
	if [ ! -d .deps ]; then mkdir .deps; fi
	hfst-lexc apertium-tr-ky.ky.lexc > .deps/ky.lexc.hfst
	hfst-twolc -R -i apertium-tr-ky.ky.twol -o .deps/ky.twol.hfst
	hfst-compose-intersect -1 .deps/ky.lexc.hfst -2 .deps/ky.twol.hfst -o .deps/tr-ky.autogen.hfst
	hfst-invert -i .deps/tr-ky.autogen.hfst -o .deps/ky-tr.automorf.hfst

	hfst-fst2fst -O -i .deps/ky-tr.automorf.hfst -o ky-tr.automorf.hfst
	hfst-fst2fst -O -i .deps/tr-ky.autogen.hfst -o tr-ky.autogen.hfst

	apertium-validate-dictionary apertium-tr-ky.tr-ky.dix
	lt-comp lr apertium-tr-ky.tr-ky.dix tr-ky.autobil.bin

	apertium-validate-transfer apertium-tr-ky.tr-ky.t1x
	apertium-preprocess-transfer apertium-tr-ky.tr-ky.t1x tr-ky.t1x.bin

	apertium-validate-modes modes.xml
	apertium-gen-modes modes.xml
	cp *.mode modes/
