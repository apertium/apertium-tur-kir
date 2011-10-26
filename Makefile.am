###############################################################################
## Makefile for Turkish--Kyrgyz
###############################################################################

VERSION=0.2.0
LANG1=tr
LANG2=ky
PREFIX1=$(LANG1)-$(LANG2)
PREFIX2=$(LANG2)-$(LANG1)

BASENAME=apertium-$(PREFIX1)

SUBDIRS = morph-tr .

TARGETS_COMMON = $(PREFIX1).autogen.hfst $(PREFIX1).autobil.bin  \
	$(PREFIX1).t1x.bin $(PREFIX1).rlx.bin \
	$(PREFIX1).mode modes 

###############################################################################
## Kyrgyz transducer
###############################################################################

.deps/ky.lexc.morf.hfst-debug: apertium-$(PREFIX1).ky.lexc
	if [ ! -d .deps ]; then mkdir .deps; fi
	@cat $< | grep -v -e 'Dir/RL' -e 'Use/Circ' > $@tmp
	hfst-lexc -f foma $@tmp -o $@.foma
	hfst-fst2fst -i $@.foma -f openfst-tropical -o $@
	rm $@tmp @.foma

.deps/ky.lexc.gen.hfst-debug: apertium-$(PREFIX1).ky.lexc
	if [ ! -d .deps ]; then mkdir .deps; fi
	@cat $< | grep -v -e 'Dir/LR' -e 'Use/Circ' > $@tmp
	hfst-lexc -f foma $@tmp -o $@.foma
	hfst-fst2fst -i $@.foma -f openfst-tropical -o $@
	rm $@tmp

.deps/ky.lexc.morf.hfst: $(BASENAME).ky.lexc
	if [ ! -d .deps ]; then mkdir .deps; fi
	@cat $< | grep -v 'Dir/RL' > $@tmp
	hfst-lexc -f foma $@tmp -o $@.foma
	hfst-fst2fst -i $@.foma -f openfst-tropical -o $@
	rm $@tmp

.deps/ky.lexc.gen.hfst: $(BASENAME).ky.lexc
	if [ ! -d .deps ]; then mkdir .deps; fi
	@cat $< | grep -v 'Dir/LR' > $@tmp
	hfst-lexc -f foma $@tmp -o $@.foma
	hfst-fst2fst -i $@.foma -f openfst-tropical -o $@
	rm $@tmp

.deps/ky.twol.hfst: $(BASENAME).ky.twol
	hfst-twolc -R -i $(BASENAME).ky.twol -o $@

# ky generator:
.deps/$(PREFIX1).autogen.hfst: .deps/ky.lexc.gen.hfst .deps/ky.twol.hfst
	hfst-compose-intersect -1 .deps/ky.lexc.gen.hfst -2 .deps/ky.twol.hfst -o $@

$(PREFIX1).autogen.hfst: .deps/$(PREFIX1).autogen.hfst
	hfst-fst2fst -w -i $< -o $@

# ky analyser:
.deps/$(PREFIX2).automorf.hfst: .deps/$(PREFIX1).autogen.hfst
	hfst-invert -i $< -o $@

$(PREFIX2).automorf.hfst: .deps/$(PREFIX2).automorf.hfst
	hfst-fst2fst -w -i $< -o $@

# debug stuff:
.deps/$(PREFIX2).automorf.hfst-debug: .deps/ky.lexc.morf.hfst-debug .deps/ky.twol.hfst
	hfst-compose-intersect -1 .deps/ky.lexc.morf.hfst-debug -2 .deps/ky.twol.hfst | hfst-invert -o $@

.deps/$(PREFIX1).autogen.hfst-debug: .deps/ky.lexc.gen.hfst-debug .deps/ky.twol.hfst
	hfst-compose-intersect -1 .deps/ky.lexc.gen.hfst-debug -2 .deps/ky.twol.hfst -o $@


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

modes/$(PREFIX1).mode: modes.xml
	apertium-validate-modes modes.xml
	apertium-gen-modes modes.xml
	cp *.mode modes/

EXTRA_DIST=$(PREFIX1).prob $(PREFIX2).prob \
           $(BASENAME).$(PREFIX1).t1x \
           $(BASENAME).$(PREFIX2).t1x \
           modes.xml

apertium_tr_kymodesdir=$(prefix)/share/apertium/modes/
apertium_tr_kydir=$(prefix)/share/apertium/$(BASENAME)/
apertium_tr_ky_DATA=$(PREFIX1).autobil.bin \
                    $(PREFIX1).prob \
		    $(PREFIX1).autogen.hfst \
		    $(PREFIX1).automorf.hfst \
		    $(PREFIX1).t1x.bin  \
		    $(PREFIX1).rlx.bin  \
		    $(BASENAME).$(PREFIX1).t1x \
		    modes.xml

noinst_DATA=modes/$(PREFIX1).mode

install-data-local:
	mv modes modes.bak
	$(prefix)/bin/apertium-gen-modes modes.xml $(BASENAME)
	rm -rf modes
	mv modes.bak modes
	test -d $(DESTDIR)$(apertium_tr_kymodesdir) || mkdir $(DESTDIR)$(apertium_tr_kymodesdir)
	$(INSTALL_DATA) $(PREFIX1).mode $(DESTDIR)$(apertium_tr_kymodesdir)
	rm $(PREFIX1).mode
	$(INSTALL_DATA) $(BASENAME).$(PREFIX1).t1x $(DESTDIR)$(apertium_tr_kydir)

CLEANFILES = -r $(TARGETS_COMMON) .deps/
