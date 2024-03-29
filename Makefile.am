###############################################################################
## Makefile for Turkish--Kyrgyz
###############################################################################

SUBDIRS=$(AP_SUBDIRS)

VERSION=0.2.0
LANG1=tur
LANG2=kir
PREFIX1=$(LANG1)-$(LANG2)
PREFIX2=$(LANG2)-$(LANG1)

BASENAME=apertium-$(PREFIX1)

TARGETS_COMMON = $(PREFIX1).autobil.bin $(PREFIX2).autobil.bin \
	$(PREFIX1).automorf.bin $(PREFIX1).autopgen.bin $(PREFIX1).autogen.bin $(PREFIX1).autogen.hfst $(PREFIX2).autogen.hfst \
	$(PREFIX1).t0x.bin $(PREFIX1).t1x.bin $(PREFIX1).t2x.bin $(PREFIX1).t3x.bin $(PREFIX1).t4x.bin $(PREFIX1).t5x.bin $(PREFIX1).t6x.bin \
	$(PREFIX2).automorf.bin $(PREFIX2).autopgen.bin $(PREFIX2).autogen.bin $(PREFIX2).t1x.bin $(PREFIX2).t2x.bin \
        $(PREFIX1).rlx.bin $(PREFIX2).rlx.bin \
        $(PREFIX1).autolex.bin $(PREFIX2).autolex.bin

# This include defines goals for install-modes, .deps/.d and .mode files:
@ap_include@

###############################################################################
## Turkish→Kyrgyz monolingual transducers
###############################################################################

.deps/$(PREFIX1).autobil.prefixes: $(PREFIX1).autobil.bin .deps/.d
	lt-print $(PREFIX1).autobil.bin | sed 's/ /@_SPACE_@/g' > .deps/$(PREFIX1).autobil.att
	hfst-txt2fst -e ε <  .deps/$(PREFIX1).autobil.att > .deps/$(PREFIX1).autobil.hfst
	hfst-project -p upper .deps/$(PREFIX1).autobil.hfst > .deps/$(PREFIX1).autobil.upper
	echo " ?* " | hfst-regexp2fst > .deps/any-symbol.hfst
	hfst-concatenate -1 .deps/$(PREFIX1).autobil.upper -2 .deps/any-symbol.hfst -o .deps/$(PREFIX1).autobil.prefixes

$(PREFIX1).automorf.bin: $(AP_SRC1)/$(LANG1).automorf.att.gz .deps/$(PREFIX1).autobil.prefixes .deps/.d
	$(ZCAT) $< | hfst-txt2fst > .deps/$(LANG1).automorf.hfst
	hfst-compose-intersect -1 .deps/$(LANG1).automorf.hfst -2 .deps/$(PREFIX1).autobil.prefixes -o .deps/$(PREFIX1).automorf.trimmed
	hfst-fst2txt -i .deps/$(PREFIX1).automorf.trimmed -o .deps/$(PREFIX1).automorf.trimmed.att
	lt-comp lr .deps/$(PREFIX1).automorf.trimmed.att $@

$(PREFIX1).autogen.hfst: $(AP_SRC2)/$(LANG2).autogen.hfst
	cp $< $@

$(PREFIX1).autogen.bin: $(AP_SRC2)/$(LANG2).autogen.bin
	cp $< $@

###############################################################################
## Kyrgyz→Turkish monolingual transducers
###############################################################################

.deps/$(PREFIX2).autobil.prefixes: $(PREFIX2).autobil.bin .deps/.d
	lt-print $(PREFIX2).autobil.bin | sed 's/ /@_SPACE_@/g' > .deps/$(PREFIX2).autobil.att
	hfst-txt2fst -e ε <  .deps/$(PREFIX2).autobil.att > .deps/$(PREFIX2).autobil.hfst
	hfst-project -p upper .deps/$(PREFIX2).autobil.hfst > .deps/$(PREFIX2).autobil.upper
	echo " ?* " | hfst-regexp2fst > .deps/any-symbol.hfst
	hfst-concatenate -1 .deps/$(PREFIX2).autobil.upper -2 .deps/any-symbol.hfst -o .deps/$(PREFIX2).autobil.prefixes

$(PREFIX2).automorf.bin: $(AP_SRC2)/$(LANG2).automorf.att.gz .deps/$(PREFIX2).autobil.prefixes .deps/.d
	$(ZCAT) $< | hfst-txt2fst > .deps/$(LANG2).automorf.hfst
	hfst-compose-intersect -1 .deps/$(LANG2).automorf.hfst -2 .deps/$(PREFIX2).autobil.prefixes -o .deps/$(PREFIX2).automorf.trimmed
	hfst-fst2txt -i .deps/$(PREFIX2).automorf.trimmed -o .deps/$(PREFIX2).automorf.trimmed.att
	lt-comp lr .deps/$(PREFIX2).automorf.trimmed.att $@

$(PREFIX2).autogen.hfst: $(AP_SRC1)/$(LANG1).autogen.hfst
	cp $< $@

$(PREFIX2).autogen.bin: $(AP_SRC1)/$(LANG1).autogen.bin
	cp $< $@

###############################################################################
## Bilingual dictionaries
###############################################################################

$(PREFIX1).autobil.bin: $(BASENAME).$(PREFIX1).dix
	apertium-validate-dictionary $<
	lt-comp lr $< $@

$(PREFIX2).autobil.bin: $(BASENAME).$(PREFIX1).dix
	apertium-validate-dictionary $< 
	lt-comp rl $< $@

###############################################################################
## Disambiguation rules 
###############################################################################

$(PREFIX1).rlx.bin: $(AP_SRC1)/apertium-$(LANG1).$(LANG1).rlx
	cg-comp $< $@

$(PREFIX2).rlx.bin: $(AP_SRC2)/apertium-$(LANG2).$(LANG2).rlx
	cg-comp $< $@


###############################################################################
## Lexical selection rules
###############################################################################

$(PREFIX1).autolex.bin: $(BASENAME).$(PREFIX1).lrx
	lrx-comp $< $@

$(PREFIX2).autolex.bin: $(BASENAME).$(PREFIX2).lrx
	lrx-comp $< $@

###############################################################################
## Structural transfer rules
###############################################################################

$(PREFIX1).t0x.bin: $(BASENAME).$(PREFIX1).t0x
	apertium-validate-transfer $(BASENAME).$(PREFIX1).t0x
	apertium-preprocess-transfer $(BASENAME).$(PREFIX1).t0x $@


$(PREFIX1).t1x.bin: $(BASENAME).$(PREFIX1).t1x
	apertium-validate-transfer $(BASENAME).$(PREFIX1).t1x
	apertium-preprocess-transfer $(BASENAME).$(PREFIX1).t1x $@

$(PREFIX1).t2x.bin: $(BASENAME).$(PREFIX1).t2x
	apertium-validate-transfer $(BASENAME).$(PREFIX1).t2x
	apertium-preprocess-transfer $(BASENAME).$(PREFIX1).t2x $@

$(PREFIX1).t3x.bin: $(BASENAME).$(PREFIX1).t3x
	apertium-validate-transfer $(BASENAME).$(PREFIX1).t3x
	apertium-preprocess-transfer $(BASENAME).$(PREFIX1).t3x $@

$(PREFIX1).t4x.bin: $(BASENAME).$(PREFIX1).t4x
	apertium-validate-interchunk $(BASENAME).$(PREFIX1).t4x
	apertium-preprocess-transfer $(BASENAME).$(PREFIX1).t4x $@

$(PREFIX1).t5x.bin: $(BASENAME).$(PREFIX1).t5x
	apertium-validate-postchunk $(BASENAME).$(PREFIX1).t5x
	apertium-preprocess-transfer $(BASENAME).$(PREFIX1).t5x $@

$(PREFIX1).t6x.bin: $(BASENAME).$(PREFIX1).t6x
	apertium-validate-transfer $(BASENAME).$(PREFIX1).t6x
	apertium-preprocess-transfer $(BASENAME).$(PREFIX1).t6x $@

$(PREFIX2).t1x.bin: $(BASENAME).$(PREFIX2).t1x
	apertium-validate-transfer $(BASENAME).$(PREFIX2).t1x
	apertium-preprocess-transfer $(BASENAME).$(PREFIX2).t1x $@

$(PREFIX2).t2x.bin: $(BASENAME).$(PREFIX2).t2x
	apertium-validate-transfer $(BASENAME).$(PREFIX2).t2x
	apertium-preprocess-transfer $(BASENAME).$(PREFIX2).t2x $@

###############################################################################
## Postgeneration dictionaries
###############################################################################

$(PREFIX1).autopgen.bin: $(AP_SRC2)/apertium-$(LANG2).post-$(LANG2).dix
	apertium-validate-dictionary $<
	lt-comp lr $< $@

$(PREFIX2).autopgen.bin: $(AP_SRC1)/apertium-$(LANG1).post-$(LANG1).dix
	apertium-validate-dictionary $< 
	lt-comp lr $< $@

###############################################################################
## Translation modes
###############################################################################

EXTRA_DIST=$(PREFIX1).prob $(PREFIX2).prob \
           $(BASENAME).$(PREFIX1).lrx \
           $(BASENAME).$(PREFIX1).dix \
           $(BASENAME).post-$(LANG1).dix \
           $(BASENAME).$(PREFIX2).lrx \
           $(BASENAME).post-$(LANG2).dix \
           $(BASENAME).$(PREFIX1).t0x \
           $(BASENAME).$(PREFIX1).t1x \
           $(BASENAME).$(PREFIX1).t6x \
           $(BASENAME).$(PREFIX2).t1x \
           $(BASENAME).$(PREFIX2).t2x \
           modes.xml

apertium_tur_kirdir=$(prefix)/share/apertium/$(BASENAME)/

apertium_tur_kir_DATA=$(TARGETS_COMMON) \
	$(BASENAME).$(PREFIX1).t1x \
	$(BASENAME).$(PREFIX1).t6x \
	$(BASENAME).$(PREFIX2).t1x \
	$(BASENAME).$(PREFIX2).t2x \
	$(PREFIX1).prob $(PREFIX2).prob

# All modes are created by the same goal, listing several will just give problems with make -j2
noinst_DATA=modes/$(PREFIX1).mode

install-data-local: install-modes


###############################################################################
## Cleanup
###############################################################################

CLEANFILES = $(TARGETS_COMMON)
clean-local: 
	-rm -rf .deps modes

test: all
	apertium-regtest test
