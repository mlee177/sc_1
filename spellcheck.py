#!/bin/env python
import pprint
import sys
root = {}
runtime = 0

# Dictionary data structure builder.
# Just a bunch of nested dictionaries containing possible next letters.
# '$' is treated as special -- it refers to the end of a valid word.
def addWord(word):
	i = 0
	current = root
	while i < len(word.strip()):
		key = word[i]
		i+=1
		while key == word[i] and i < len(word):
			key += word[i]
			i += 1
		current = current.setdefault(key,{}) 
	current['$'] = '$'

# Called from main to jumpstart things.
def checkWord(word):
	print(word)
	return checkWordHelper(word, root, "")

# Counts the number of repeated characters in the beginning of a word
def countCharRepeats(word):
	if len(word) == 0:
		return 0
	elif len(word) == 1:
		return 1
	else:
		i = 1
		while i < len(word) and word[i-1].lower() == word[i].lower():
			i+=1
		return i

def countCharRepeatsVowels(word):
	if len(word) == 0:
		return 0
	elif len(word) == 1 and isVowel(word[0]):
		return 1
	else:
		count = 0
		while count < len(word):
			if isVowel(word[count]):
				count += 1
			else:
				return count
		return count

# Returns true if the length 1 string given is a vowel.
def isVowel(char):
	return True if char.lower() in 'aeiou' else False

# Returns true if a word/key is composed entirely of vowels.
def keyIsVowels(key):
	for char in key:
		if not isVowel(char):
			return False
	return True
	
# Primary recursive function.
# Overview:
#	*Check for repeats
#	*If consonant, do a slightly less complex recursive loop
# 	*If vowel, do a slightly more complex recursive loop <-- very time consuming.
#	 n = repeat count, m = keys at the current dictionary level, 
#	Something like O(n^2 * m)? Thankfully, n and m will tend to be small. 
def checkWordHelper(remainingword, currentdict, currentoutput):
	#print("    HELPER rw:'{}',co:'{}'".format(remainingword,currentoutput))
	
	# Check end of word
	if len(remainingword) == 0:
		if currentdict.get('$'):
			return currentoutput #whole word found
		else:
			return 1 # Substring found
	

	# Building key
	currentchar = remainingword[0]
	count = countCharRepeats(remainingword) # 'aaab' would return 3
	vowelcount = countCharRepeatsVowels(remainingword)

	if not isVowel(currentchar):
		# Test different repeat counts, starting from the highest (what was given)
		for i in range(count+1): 
			repeatedsubstring = remainingword[:count-i].lower()
			if(repeatedsubstring):
				for key in [(key.lower(),key) for key in currentdict.keys()]:
					if repeatedsubstring == key[1]:
						output = checkWordHelper(remainingword[i+len(key[1]):],currentdict.get(repeatedsubstring),
								currentoutput + repeatedsubstring)
						if output is not 0 and output is not 1:
							return output
			else:
				return 1


	else:
		# Time consuming loop
		# When all is said and done, checks all combinations of repeats and vowels 
		# That are possible within the given dictionary level and repeat length..
		for i in range(vowelcount): # n
			keys = [ key for key in currentdict.keys() if len(key) == vowelcount-i and keyIsVowels(key)] # m
			if keys:
				for key in keys:
					output = checkWordHelper(remainingword[len(key):],currentdict.get(key),
							currentoutput + key) 
					if output is not 0 and output is not 1:
						return output
			
			# If no keys were found, or if the loop didn't find a valid word, decrement by one and try again.
			if(vowelcount > 1):
				output = checkWordHelper(remainingword[1:],currentdict,currentoutput)
				if output is not 0 and output is not 1:
					return output
			else:
				return 0
				

	# Loops found nothing.
	return 0
	
if __name__ == "__main__":
	dictfilename = "wordsEn.txt"

	file = open(dictfilename,'r')

	for word in file:
		addWord(word)

	#print(sys.getsizeof(root))
	print("Enter nothing or press Ctrl + C to end.")

	word = input('>')
	while len(word) > 0:
		output = checkWord(word)
		if output is 0:
			print("No suggestion (not found)")
		elif output is 1:
			print("No suggestion (substring)")
		else:
			print(output)

		word = input('>')

	#pprint.pprint(root)
