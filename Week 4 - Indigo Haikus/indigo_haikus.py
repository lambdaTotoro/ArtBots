from nltk.parse.generate import generate, demo_grammar
from nltk import CFG

import random
import re
import requests
import syllables

def main_phrases(name, othername = None):
	
	phrase_grammar = f"""
		S -> '{name}!'
		S -> 'Go, {name}!'
		S -> 'Show them, {name}!'
		S -> 'I chose you, {name}!'
		S -> 'You can do it, {name}!'
	"""
	
	grammar = CFG.fromstring(phrase_grammar)
	phrases = list(generate(grammar))
	shortlist = list(filter(lambda x: (syllables.estimate(x[0]) == 5), phrases))
	return shortlist[0]

def single_phrases(name, types = None, evolutions = None, attacks = None):
	phrase_grammar = f"""
	   
		
	"""
	
	if attacks != None:
		for attack in attacks:
			phrase_grammar += f"""
				S -> 'Use {attack}!'
				S -> '{attack}, now!'
			"""
	
	grammar = CFG.fromstring(phrase_grammar)
	return generate(grammar)
	
def find_attacks(name):
	
	moveset = None
	
	regex_move = '\(move\)"><span style="color:#000;">([A-Za-z\s\-]+)</span>'
	regex_move_tmhm = 'M\d\d</span></a>\n</td>\n.{1,150}\(move\)"><span style="color:#000;">([A-Za-z\s\-]+)</span>'

	
	for gen in ["I","II","III","IV","V","VI","VII"]:
		r = requests.get(f'https://bulbapedia.bulbagarden.net/wiki/{name}_(Pok%C3%A9mon)/Generation_{gen}_learnset')
		if r.status_code == 200:
			if moveset == None:
				moveset = []
				
			src = r.text
			moves_lvl = set(re.findall(regex_move, src))
			moves_tmhm = set(re.findall(regex_move_tmhm, src))			
			moves = list(moves_lvl - moves_tmhm)
			
			for move in moves:
				moveset.append(move)
	
	assert(moveset != None)
	moveset = list(set(moveset))
	return moveset

#daname = "Pikachu"

#for p in single_phrases(daname, attacks = find_attacks(daname)):
#	print(p)

for name in ["Tom", "Benny", "Jennifer", "Benedictus", "Franziska-Jasmin"]:
	print(main_phrases(name)[0])
