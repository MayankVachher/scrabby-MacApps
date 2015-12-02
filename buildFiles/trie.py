#Trie implementation using child pointers in hash table (dictionary)
class TrieNode(object):

	def __init__(self, char):
		self.char = char
		self.children = {}

	def setChild(self, node):
		self.children[node.char] = node

	def getChild(self, character):
		return self.children.get(character)

class Trie(object):

	def __init__(self):
		self.root = TrieNode("R")

	def addWord(self,word):	  
		current = self.root

		for item in word:
			nextNode = current.getChild(item)
			if(nextNode is not None):
				current = nextNode
			else:
				current.setChild(TrieNode(item))
				current = current.getChild(item)

		#Add special end of word character
		current.setChild(TrieNode('{')) 
		current = current.children['{']


	def query(self, word):
		current = self.root

		#Handle case when word is not present anywhere
		for item in word:
			nextNode = current.getChild(item)
			if(nextNode is not None):
				current = nextNode
			else:
				return False

		#Handle case when word is present only as a prefix
		nextNode = current.getChild('{')
		if(nextNode is not None):
			return True
		else:
			return False

#Trie implementation ends


