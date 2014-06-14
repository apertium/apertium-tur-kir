
FILE=`basename $1`;
CORP=$1
PAIR=tur-kir

cat $CORP | apertium-destxt | apertium -f none -d ../ $PAIR-morph | sed 's/\$\W*\^/$\n^/g' | tee /tmp/$PAIR.morph |\
	cg-proc ../$PAIR.rlx.bin | tee /tmp/$PAIR.disam |\
	cg-proc -n -1 ../$PAIR.rlx.bin |\
	apertium-pretransfer | sed 's/\$\W*\^/$\n^/g' | tee /tmp/$PAIR.pretransfer |\
	lt-proc -b ../$PAIR.autobil.bin | tee /tmp/$PAIR.biltrans |\
	lrx-proc -m ../$PAIR.autolex.bin | tee /tmp/$PAIR.lextor |\
	apertium-transfer -b ../apertium-tur-kir.tur-kir.t0x  ../tur-kir.t0x.bin |\
	apertium-transfer -n ../apertium-tur-kir.tur-kir.t1x  ../tur-kir.t1x.bin |\
	apertium-transfer -n ../apertium-tur-kir.tur-kir.t2x  ../tur-kir.t2x.bin |\
	apertium-transfer -n ../apertium-tur-kir.tur-kir.t3x  ../tur-kir.t3x.bin |\
	apertium-interchunk ../apertium-tur-kir.tur-kir.t4x  ../tur-kir.t4x.bin |\
	apertium-postchunk ../apertium-tur-kir.tur-kir.t5x  ../tur-kir.t5x.bin |\
	apertium-transfer -n ../apertium-tur-kir.tur-kir.t6x  ../tur-kir.t6x.bin | tee /tmp/$PAIR.transfer |\
	lt-proc -d ../tur-kir.autogen.bin > /tmp/$PAIR.gener 


WORDS=`cat /tmp/$PAIR.morph | wc -l`;
KNOWN=`cat /tmp/$PAIR.morph | grep -v '\*' | wc -l`;
ANALYSES=`cat /tmp/$PAIR.morph | cut -f2- -d'/' | sed 's/\//\n/g' | wc -l`; 
DISAMANALYSES=`cat /tmp/$PAIR.disam | cut -f2- -d'/' | sed 's/\//\n/g' | wc -l`;
PRETRANSFER=`cat /tmp/$PAIR.pretransfer | wc -l`;
BILTRANS=`cat /tmp/$PAIR.biltrans | cut -f2- -d'/' | sed 's/\//\n/g' | wc -l`;
LEXTOR=`cat /tmp/$PAIR.lextor | cut -f2- -d'/' | sed 's/\//\n/g' | wc -l`;
GENFAIL=`cat /tmp/$PAIR.gener | grep '#' | wc -l`;

COVERAGE=`calc $KNOWN/$WORDS\*100`;
AVGAMBIG=`calc $ANALYSES/$WORDS`;
DISAMBIG=`calc $DISAMANALYSES/$WORDS`;
TESTVOC=`calc $GENFAIL/$PRETRANSFER\*100`;
BILAMBIG=`calc $BILTRANS/$PRETRANSFER`;
LEXAMBIG=`calc $LEXTOR/$PRETRANSFER`;

echo $WORDS" "$KNOWN" "$COVERAGE
echo $WORDS" "$ANALYSES" "$AVGAMBIG
echo $WORDS" "$DISAMANALYSES" "$DISAMBIG
echo $PRETRANSFER" "$BILTRANS" "$BILAMBIG
echo $PRETRANSFER" "$LEXTOR" "$LEXAMBIG
echo $PRETRANSFER" "$GENFAIL" "$TESTVOC

DATE=`date +%Y-%m-%d\|%H:%M`;

echo $DATE" "$FILE" "$WORDS" "$KNOWN" "$ANALYSES" "$PRETRANSFER" "$BILTRANS" "$LEXTOR" "$GENFAIL" "$COVERAGE" "$AVGAMBIG" "$DISAMBIG" "$BILAMBIG" "$LEXAMBIG" "$TESTVOC >> history.log
