#!/usr/bin/env python3

class orthoConv:

	latinDigraphs = {"ağ": "оо", "uv": "уу", "uğ": "уу"}
	latinYod = {"yo": "ё", "ye": "е", "yu": "ю", "ya": "я"}
	latinWordInit = {"e": "э"}
	latinLetters = {"a": "а", "b": "б", "c": "ж", "ç": "ч", "d": "д", "e": "е", "f": "ф", "g": "г", "ğ": "г", "h": "х", "i": "и", "ı": "ы", "j": "ж", "k": "к", "l": "л", "m": "м", "n": "н", "o": "о", "ö": "ө", "p": "п", "q": "к", "r": "р", "s": "с", "t": "т", "u": "у", "ü": "ү", "v": "в", "x": "х", "y": "й", "z": "з"}

	#cyrillicLetters = {"ў": "o'", "ғ": "g'", "ч": "ch", "ш": "sh", "ц": "ts", "ё": "yo", "е": "ye", "ю": "yu", "я": "ya", "э": "e", "а": "a", "б": "b", "д": "d", "е": "e", "ф": "f", "г": "g", "ҳ": "h", "и": "i", "ж": "j", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "қ": "q", "р": "r", "с": "s", "т": "t", "у": "u", "в": "v", "х": "x", "й": "y", "з": "z", "ъ": "'", "ь": ""}


	text = ""

	def __init__(self, text):
		self.text = text

	def convert(self, text, replacements, wordInit=False):
		if wordInit:
			inText = text
			text = text[0]
		for key in replacements:
			text = text.replace(key, replacements[key])
			Key = key
			Key = Key.replace(Key[0], Key[0].upper())
			Replacement = replacements[key]
			if len(Replacement) >= 1:
				Replacement = Replacement.replace(Replacement[0], Replacement[0].upper())
			text = text.replace(Key, Replacement)

			KEY = key.upper()
			REPLACEMENT = replacements[key]
			if len(REPLACEMENT) >= 1:
				REPLACEMENT = REPLACEMENT.replace(REPLACEMENT[0], REPLACEMENT[0].upper())
			text = text.replace(KEY, REPLACEMENT)
		if wordInit:
			outText = text[0] + inText[1:]
		else:
			outText = text
		return outText

	def latin2cyrillic(self):
		outText = self.text
		outText = self.convert(outText, self.latinDigraphs)
		outText = self.convert(outText, self.latinYod)
		outText = self.convert(outText, self.latinWordInit, wordInit=True)
		outText = self.convert(outText, self.latinLetters)
		return outText

	#def cyrillic2latin(self):
	#	outText = self.text.decode('utf-8')
	#	#outText = self.text
	#	outText = self.convert(outText, self.cyrillicLetters)
	#	return outText

if __name__ == "__main__":
	import sys
	if len(sys.argv) > 1:
		for word in sys.argv[1:]:
			thisWord = orthoConv(word)
			print("%s: %s" % (word, thisWord.latin2cyrillic()))
	else:
		print("Usage: %s word" % sys.argv[0])

