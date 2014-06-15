TMPDIR=/tmp

for i in *.tur.txt; do 
	prefix=`echo $i | cut -f1 -d'.'`;

	cat $i | apertium -d ../ tur-kir > $TMPDIR/$prefix.tur-kir.txt
	for j in $prefix.kir.*; do
		echo -ne "$prefix\t$j\t";
		apertium-eval-translator -t $TMPDIR/$prefix.tur-kir.txt -r $j | grep -e WER -e PER | head -2 | tr '\n' '\t' | sed 's/Word error rate//g' | sed 's/Position-independent word error rate//g'
		echo ""
	done
done
