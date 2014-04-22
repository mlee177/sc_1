#!/bin/env
import pprint
root = {}
debug = True

# $ is treated as a special character and represents the end of a word
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


def checkWord(word):
	print(word)
	return checkWordHelper(word, root, "")

def countCharRepeats(word):
	if len(word) > 1:
		firstchar = word[0]
		count = 1
		next = word[count]
		while next.lower() == firstchar.lower() and len(word) > count + 1 :
			count+=1
			next = word[count]
		return count
	elif len(word)==1:
		return 1
	else:
		return 0

def countCharRepeatsVowels(word):
	if len(word)>1:
		count = 0
		while isVowel(word[count]):
			count+=1

		return count
	elif len(word)==1 and isVowel(word):
		return 1
	else: 
		return 0

def isVowel(char):
	return True if char.lower() in 'aeiou' else False

def keyIsVowels(key):
	for char in key:
		if not isVowel(char):
			return False
	return True
	
def checkWordHelper(remainingword, currentdict, currentoutput):
	if(debug):
		print("HELP    rw:'{}' co:'{}'".format(remainingword,currentoutput))
	
	# Check end of word
	if len(remainingword) == 0:
		if currentdict.get('$'):
			return currentoutput
		else:
			return 1 # Substring found
	

	# Building key
	currentchar = remainingword[0]
	count = countCharRepeats(remainingword) # 'aaab' would return 3
		
	
	print("count {} ".format(count))
	if not isVowel(currentchar):
		for i in range(count+1): 
			repeatedsubstring = remainingword[:count-i].lower()
			print("repeatedsubstring : {}".format(repeatedsubstring))
			if(repeatedsubstring):
				for key in [(key.lower(),key) for key in currentdict.keys()]:
					if repeatedsubstring == key[1]:
						output = checkWordHelper(remainingword[i+len(key[1]):],currentdict.get(repeatedsubstring),
								currentoutput + repeatedsubstring)
						if output is not 0 and output is not 1:
							return output
			else:
				return 1

	else:	# Vowel!
		for i in range(count+1): # 0,1,2,3 .. count
			if count-i > 0: 
				for key in [ key for key in currentdict.keys() if len(key) == count-i and keyIsVowels(key) ]:
					print("Vowel key {}".format(key)
					output = checkWordHelper(remainingword[i+len(key):], currentdict.get(key),
							currentoutput + key)
					if output is not 0 and output is not 1:
						return output

			else:
				return 1
		
						




if __name__ == "__main__":
	dictfilename = "wordsEn.txt"

	file = open(dictfilename,'r')

	for word in file:
		addWord(word)

	print("Enter nothing or press Ctrl + C to end.")
	if(debug):
		print("0 = not found, 1 = substring of valid word")

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
