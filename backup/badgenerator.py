#!/bin/env python
import random


def changeCase(char):
	return char.lower if char.isupper()  else char.upper()

def repeat(char):
	return char * random.randint(1,4)


def changevowel(char):
	return random.choice([vowel for vowel in 'aeiou' if vowel is not char])

for i in range(50):
	word = random.choice(list(open('wordsEn.txt'))).strip()
	

	output = ""
	for char in word:
		if char in 'aeiouAEIOU':
			output += changevowel(char)
		else:
			output += char

	output2 = ""
	for char in output:
		output2 += repeat(char)

	output = ""
	for char in output2:
		if random.randint(0,1):
			output += changeCase(char)
		else:
			output += char

	print(word)
	print(output)

print("")



