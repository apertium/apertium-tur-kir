all:
	apertium-validate-dictionary apertium-tr-ky.tr-ky.dix
	lt-comp lr apertium-tr-ky.tr-ky.dix tr-ky.autobil.bin

	apertium-validate-modes modes.xml
	apertium-gen-modes modes.xml
	#cp *.mode modes/
