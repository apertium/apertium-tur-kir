all: tr-ky.autobil.bin
	if [ ! -d .deps ]; then mkdir .deps; fi
	cat apertium-tr-ky.ky.lexc | grep -v 'Dir/RL' | hfst-lexc > .deps/ky.lexc.morf.hfst
	cat apertium-tr-ky.ky.lexc | grep -v 'Dir/LR' | hfst-lexc > .deps/ky.lexc.gen.hfst
	hfst-twolc -R -i apertium-tr-ky.ky.twol -o .deps/ky.twol.hfst
	hfst-compose-intersect -1 .deps/ky.lexc.gen.hfst -2 .deps/ky.twol.hfst -o .deps/tr-ky.autogen.hfst
	hfst-compose-intersect -1 .deps/ky.lexc.morf.hfst -2 .deps/ky.twol.hfst | hfst-invert -o .deps/ky-tr.automorf.hfst

	hfst-fst2fst -O -i .deps/ky-tr.automorf.hfst -o ky-tr.automorf.hfst
	hfst-fst2fst -O -i .deps/tr-ky.autogen.hfst -o tr-ky.autogen.hfst

	cg-comp apertium-tr-ky.tr-ky.rlx tr-ky.rlx.bin

	apertium-validate-transfer apertium-tr-ky.tr-ky.t1x
	apertium-preprocess-transfer apertium-tr-ky.tr-ky.t1x tr-ky.t1x.bin

	apertium-validate-modes modes.xml
	apertium-gen-modes modes.xml
	cp *.mode modes/

tr-ky.autobil.bin:

	if [ ! -d .deps ]; then mkdir .deps; fi
	xsltproc lexchoicebil.xsl apertium-tr-ky.tr-ky.dix > .deps/apertium-tr-ky.tr-ky.dix
	apertium-validate-dictionary .deps/apertium-tr-ky.tr-ky.dix
	lt-comp lr .deps/apertium-tr-ky.tr-ky.dix tr-ky.autobil.bin

