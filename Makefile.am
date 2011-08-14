###############################################################################
## Makefile for Turkish--Kyrgyz
###############################################################################

VERSION=0.2.0
LANG1=tr
LANG2=ky
PREFIX1=$(LANG1)-$(LANG2)
PREFIX2=$(LANG2)-$(LANG1)

BASENAME=apertium-$(PREFIX1)

SUBDIRS = . morph-tr

TARGETS_COMMON = $(PREFIX2).automorf.hfst $(PREFIX1).autogen.hfst $(PREFIX1).autobil.bin $(PREFIX2).autobil.bin  \
	$(PREFIX1).t1x.bin $(PREFIX1).rlx.bin \
	$(PREFIX1).mode modes 

###############################################################################
## Kyrgyz transducer
###############################################################################

.deps/ky.lexc.morf.hfst-debug: apertium-tr-ky.ky.lexc
	@cat $< | grep -v -e 'Dir/RL' -e 'Use/Circ' | hfst-lexc -o $@

.deps/ky.lexc.gen.hfst-debug: apertium-tr-ky.ky.lexc
	@cat $< | grep -v -e 'Dir/LR' -e 'Use/Circ' | hfst-lexc -o $@

.deps/ky.lexc.morf.hfst: apertium-tr-ky.ky.lexc
	@cat $< | grep -v 'Dir/RL' | hfst-lexc -o $@

.deps/ky.lexc.gen.hfst: apertium-tr-ky.ky.lexc
	@cat $< | grep -v 'Dir/LR' | hfst-lexc -o $@

.deps/ky.twol.hfst: apertium-tr-ky.ky.twol
	hfst-twolc -R -i apertium-tr-ky.ky.twol -o $@

.deps/ky-tr.automorf.hfst-debug: .deps/ky.lexc.morf.hfst-debug .deps/ky.twol.hfst
	hfst-compose-intersect -1 .deps/ky.lexc.morf.hfst-debug -2 .deps/ky.twol.hfst | hfst-invert -o $@

.deps/tr-ky.autogen.hfst-debug: .deps/ky.lexc.gen.hfst-debug .deps/ky.twol.hfst
	hfst-compose-intersect -1 .deps/ky.lexc.gen.hfst-debug -2 .deps/ky.twol.hfst -o $@

.deps/ky-tr.automorf.hfst: .deps/ky.lexc.morf.hfst .deps/ky.twol.hfst
	hfst-compose-intersect -1 .deps/ky.lexc.morf.hfst -2 .deps/ky.twol.hfst | hfst-invert -o $@

.deps/tr-ky.autogen.hfst: .deps/ky.lexc.gen.hfst .deps/ky.twol.hfst
	hfst-compose-intersect -1 .deps/ky.lexc.gen.hfst -2 .deps/ky.twol.hfst -o $@

$(PREFIX1).autogen.hfst: .deps/tr-ky.autogen.hfst .deps/tr-ky.autogen.hfst-debug
	hfst-fst2fst -w -i $< -o $@

$(PREFIX2).automorf.hfst: .deps/ky-tr.automorf.hfst .deps/ky-tr.automorf.hfst-debug
	hfst-fst2fst -w -i $< -o $@

###############################################################################
## Bilingual dictionaries
###############################################################################

.deps/$(BASENAME).$(PREFIX1).dix: $(BASENAME).$(PREFIX1).dix lexchoicebil.xsl
	if [ ! -d .deps ]; then mkdir .deps; fi
	xsltproc lexchoicebil.xsl $(BASENAME).$(PREFIX1).dix > $@

$(PREFIX1).autobil.bin: .deps/$(BASENAME).$(PREFIX1).dix
	apertium-validate-dictionary .deps/$(BASENAME).$(PREFIX1).dix
	lt-comp lr .deps/$(BASENAME).$(PREFIX1).dix $@

$(PREFIX2).autobil.bin: .deps/$(BASENAME).$(PREFIX1).dix
	apertium-validate-dictionary $(BASENAME).$(PREFIX1).dix
	lt-comp rl .deps/$(BASENAME).$(PREFIX1).dix $@

###############################################################################
## Constraint grammar disambiguation
###############################################################################

$(PREFIX1).rlx.bin: $(BASENAME).$(PREFIX1).rlx
	cg-comp $(BASENAME).$(PREFIX1).rlx $@

#$(PREFIX2).rlx.bin: $(BASENAME).$(PREFIX1).rlx
#	cg-comp $(BASENAME).$(PREFIX1).rlx $@

###############################################################################
## Structural transfer
###############################################################################

$(PREFIX1).t1x.bin: $(BASENAME).$(PREFIX1).t1x
	apertium-validate-transfer $(BASENAME).$(PREFIX1).t1x
	apertium-preprocess-transfer $(BASENAME).$(PREFIX1).t1x $@

#$(PREFIX2).t1x.bin: $(BASENAME).$(PREFIX2).t1x
#	apertium-validate-transfer $(BASENAME).$(PREFIX2).t1x
#	apertium-preprocess-transfer $(BASENAME).$(PREFIX2).t1x $@

###############################################################################
## Translation modes
###############################################################################

$(PREFIX1).mode: modes.xml
	apertium-gen-modes modes.xml
	cp *.mode modes/

#$(PREFIX2).mode: modes.xml
#	apertium-gen-modes modes.xml
#	cp *.mode modes/

EXTRA_DIST=$(PREFIX1).prob $(PREFIX2).prob \
           $(BASENAME).$(PREFIX1).t1x \
           $(BASENAME).$(PREFIX2).t1x \
           modes.xml

apertium_tr_kymodesdir=$(prefix)/share/apertium/modes/
apertium_tr_kydir=$(prefix)/share/apertium/apertium-$(PREFIX1)/
apertium_tr_ky_DATA=$(PREFIX1).autobil.bin $(PREFIX2).autobil.bin \
                    $(PREFIX1).prob $(PREFIX2).prob \
		    $(PREFIX1).autogen.hfst \
		    $(PREFIX2).automorf.hfst \
		    $(PREFIX1).t1x.bin  \
		    $(PREFIX1).rlx.bin  \
		    $(BASENAME).$(PREFIX1).t1x \
		    $(PREFIX1).mode

install-data-local:
	$(prefix)/bin/apertium-gen-modes modes.xml apertium-$(PREFIX1)
	$(INSTALL_DATA) $(PREFIX1).mode $(apertium_tr_kymodesdir)
	$(INSTALL_DATA) $(PREFIX2).mode $(apertium_tr_kymodesdir)
	$(INSTALL_DATA) $(BASENAME).$(PREFIX1).t1x $(BASENAME).$(PREFIX2).t1x $(apertium_tr_kydir)

CLEANFILES = -r $(TARGETS_COMMON) .deps/

