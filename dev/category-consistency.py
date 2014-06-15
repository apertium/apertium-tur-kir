# What does this script do ?
# - It tries to check that the category for a lemma on the right side of
#   a bilingual dictionary agrees with one of the categories for that 
#   lemma in the corresponding lexc file.
#
# How does it do that ? 
# - Look at the comments ^^
#
#

import sys ;

# Correspondences between the lexc file and the bilingual dictionary
lexc_bidix = { 
	'V-TV': '<s n="v"/><s n="tv"/>',
	'V-INFL-TV': '<s n="v"/><s n="tv"/>',
	'V-IV': '<s n="v"/><s n="iv"/>',
	'V-INFL-IV': '<s n="v"/><s n="iv"/>',
	'N-INFL': '<s n="n"/>',
	'N-INFL-3PX-COMPOUND': '<s n="n"/>',
	'ADV': '<s n="adv"/>',
	'ADJ': '<s n="adj"/>',
	'A1': '<s n="adj"/>',
	'A2': '<s n="adj"/>',
	'A3': '<s n="adj"/>',
	'A4': '<s n="adj"/>',
	'A5': '<s n="adj"/>'
};

# Correspondences between the bilingual dictionary and the lexc file
bidix_lexc= { 
	'<s n="v"/><s n="tv"/>': ['V-TV', 'V-INFL-TV', 'V-INFL-IV-IRREG-CAUS', 'V-INFL-TV-NO-CAUS'],
	'<s n="v"/><s n="iv"/>': ['V-IV', 'V-INFL-IV'],
	'<s n="n"/>': ['N-INFL', 'N-INFL-3PX-COMPOUND'],
	'<s n="adj"/>': ['ADJ', 'A1', 'A2', 'A3', 'A4', 'A5'],
	'<s n="adv"/>': ['ADV']
};

inlexicon = False;
inroot = False;
stemlexicons = []; 
currentlex = '';

lexc_stems = [];
stem_cont = {};

# For each line in the lexc file
for line in open(sys.argv[1]).readlines(): #{
	#print(inlexicon, inroot, stemlexicons, currentlex, line);
	if line.count('LEXICON Root') > 0: #{
		inroot = True;
		continue;
	#}
	if line.count('LEXICON') and inroot: #{
		inroot = False;
	#}

	# If we are in the Root lexicon then we want to make a list of the stem lexicons 
	if inroot and line[0] != '!': #{
		stemlexicons.append(line.strip().strip('; '));
	#}

	if line.count('LEXICON') > 0: #{
		inlexicon = False;
		nom = line.split(' ')[1].strip(); 

		# Is this a stem lexicon or another continuation lexicon ? 
		if nom in stemlexicons: #{
			currentlex = nom;
			inlexicon = True;
		#}	
	#}

	# If we are in a stem lexicon and it looks like this line contains an entry
	if inlexicon == True and line.count(':') > 0 and line.count(';') > 0 and line[0] != '!':  #{
		lema = line.split(':')[0].replace('%','');
		cont = line.replace('% ','%').split(' ')[1];
		bidixcat = '';
		if cont in lexc_bidix: #{
			bidixcat = lexc_bidix[cont];
		#}
		if lema not in stem_cont: #{
			stem_cont[lema] = [];
		#}

		# Add the lemma and the bidix category to lexc_stems, e.g. lexc_stems[('foo', '<s n="n"/>')];
		lexc_stems.append((lema, bidixcat)); 

		# Add the lemma and the possible continuations to stem_cont e.g. stem_cont['foo'] = ['N1', 'V-TV'];
		stem_cont[lema].append(cont); 

		#print(currentlex + '\t' + cont + '\t' + lema);
	#}
#}

dix = ''; # Clean output
suspicious = ''; # Suspicious output

# For each line in the bilingual dictionary
for line in open(sys.argv[2]).readlines(): #{

	# If the line doesn't contain a right side, skip it and add it to the clean output
	if line.count('<r>') < 1: #{
		dix = dix + line;	
	else: #{
		right = line.split('<r>')[1].split('</r>')[0].replace('<b/>', ' ').replace('<b />', ' ');
		lema = right.split('<')[0];
		tags = '<' + '<'.join(right.split('<')[1:]);

		# Conditions:
		# 1) The combination of lemma and tags has not been found in the lexc file
		# 2) The lemma has been found in the lexc file
		# 3) The tags are among those that we are checking
		if (lema, tags) not in lexc_stems and lema in stem_cont and tags in bidix_lexc: #{
			# This is a suspicious entry, it is in the lexc file and in the bidix, but the tags 
			# do not agree.
			print('suspicious: ', lema, tags, stem_cont[lema], file=sys.stderr);
			suspicious = suspicious + line;
		else: #{
			# Either not suspicious or we are not checking those tags.
			dix = dix + line;
		#}
	#}

#}

print(dix);
print('<!--');
print(suspicious.replace('--','@@'));
print('-->');
