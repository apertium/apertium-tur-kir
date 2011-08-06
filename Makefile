all: deps bidix other modes lexc twolc transducer

deps: 
	if [ ! -d .deps ]; then mkdir .deps; fi

bidix:
	xsltproc lexchoicebil.xsl apertium-tr-ky.tr-ky.dix > .deps/apertium-tr-ky.tr-ky.dix
	apertium-validate-dictionary .deps/apertium-tr-ky.tr-ky.dix
	lt-comp lr .deps/apertium-tr-ky.tr-ky.dix tr-ky.autobil.bin
	cg-comp apertium-tr-ky.tr-ky.rlx tr-ky.rlx.bin

other:
	apertium-validate-transfer apertium-tr-ky.tr-ky.t1x
	apertium-preprocess-transfer apertium-tr-ky.tr-ky.t1x tr-ky.t1x.bin

modes:
	apertium-validate-modes modes.xml
	apertium-gen-modes modes.xml
	cp *.mode modes/

lexc:
	cat apertium-tr-ky.ky.lexc | grep -v 'Dir/RL' | hfst-lexc > .deps/ky.lexc.morf.hfst
	cat apertium-tr-ky.ky.lexc | grep -v 'Dir/LR' | hfst-lexc > .deps/ky.lexc.gen.hfst

twolc:
	hfst-twolc -R -i apertium-tr-ky.ky.twol -o .deps/ky.twol.hfst

onlytwolc: twolc transducer

onlylexc: lexc transducer

transducer:
	hfst-compose-intersect -1 .deps/ky.lexc.gen.hfst -2 .deps/ky.twol.hfst -o .deps/tr-ky.autogen.hfst
	hfst-compose-intersect -1 .deps/ky.lexc.morf.hfst -2 .deps/ky.twol.hfst | hfst-invert -o .deps/ky-tr.automorf.hfst

	hfst-fst2fst -w -i .deps/ky-tr.automorf.hfst -o ky-tr.automorf.hfst
	hfst-fst2fst -w -i .deps/tr-ky.autogen.hfst -o tr-ky.autogen.hfst

clean:
	rm -rf ky-tr.automorf.hfst tr-ky.autogen.hfst .deps tr-ky.rlx.bin tr-ky.t1x.bin modes/ tr-ky.autobil.bin
