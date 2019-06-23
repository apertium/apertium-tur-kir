import sys, os, re

def monofy(line,left=True, verbose=False):
    line = re.sub("<e[^>]*>", "<e>", line)
    dic = { '<s n="adj"/>':'A1',
            '<s n="adj"/><s n="subst"/>':'A1',
            '<s n="adv"/>':"ADV",
            '<s n="n"/>':"N1",
            '<s n="n"/><s n="attr"/>':"N1",
            '<s n="np"/><s n="top"/>':"NP-TOP",
	    '<s n="post"/>':"POST",
            '<s n="np"/><s n="cog"/><s n="mf"/>':"NP-COG-MF",
            '<s n="np"/><s n="org"/>':"NP-ORG",
            '<s n="np"/><s n="al"/>':"NP-AL",
            '<s n="prn"/><s n="itg"/>':"PRON-ITG",
            '<s n="prn"/><s n="pers"/>':"PRON-PERS",
            '<s n="det"/><s n="itg"/>':"DET-ITG",
            '<s n="adv"/><s n="itg"/>':"ADV-ITG",
            '<s n="v"/><s n="iv"/>':"V-IV",
            '<s n="cnjcoo"/>':"CC",
            '<s n="ij"/>':"INTERJ",
            '<s n="cnjsub"/>':"CS",
            '<s n="np"/><s n="ant"/><s n="m"/>':'NP-ANT-M',
            '<s n="np"/><s n="ant"/><s n="f"/>':'NP-ANT-F',
            '<s n="cnjadv"/>':"CA",
            '<s n="v"/><s n="tv"/>':"V-TV",
            '<s n="v"/><s n="tv"/><s n="pass"/>':"V-TV",
            '<s n="v"/><s n="tv"/><s n="caus"/>':"V-TV",
            '<s n="v"/><s n="iv"/><s n="pass"/>':"V-IV",
            '<s n="v"/><s n="iv"/><s n="caus"/>':"V-IV",
	    '<s n="det"/><s n="qnt"/>':"DET-QNT",
	    '<s n="det"/><s n="dem"/>':"DET-DEM",
	    '<s n="cog"/><s n="mf"/>':"NP-COG-MF",
            '<s n="prn"/><s n="qnt"/>':"PRON-QNT",
            '<s n="prn"/><s n="dem"/>':"PRON-DEM",
            '<s n="num"/><s n="num"/>':"NUM"
}

    if left:
        word = line.partition("<l>")[2].partition("<s")[0]
        tags= "".join(line.partition("<s")[1:]).partition("</l>")[0]
    else:
        word = line.partition("<l>")[2].partition("<s")[0]
        tags= "".join(line.partition("<r>")[2].partition("<s")[1:]).partition("</r>")[0]
    #word = word.replace("<b/>","% ")
    word = re.sub("<b */>", "% ", word)
    if verbose:
        if tags not in dic:
            print(tags, "not in dictionary")
    entry = word + ":" + word + " " + dic[tags] + " ; !"
    return entry


if __name__=="__main__":
    left, verbose, debug = True, False, False
    if "-tur" in sys.argv: left=False
    if "-verbose" in sys.argv or "-v" in sys.argv: verbose=True
    if "-debug" in sys.argv or "-d" in sys.argv: debug=True
    d = os.path.dirname(__file__)
    if left:
        filename = os.path.join(d, '../../apertium-kir/apertium-kir.kir.lexc')
    else:
        filename = os.path.join(d, '../../apertium-tur/apertium-tur.tur.lexc')
    text = "".join([x for x in open(filename).readlines() if "V-TD" not in x])
    for line in sys.stdin.readlines():
        if "<e" in line:
            try:
                m = monofy(line, left, verbose)
                search = re.search(m.replace(" ", " *"), text)
                if not search:
                    if not debug:
                        sys.stdout.write(m + "\n")
            except KeyError:
                if verbose:
                    print("Unknown tags:",line)
                continue

