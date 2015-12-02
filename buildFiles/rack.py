from tile import *
from random import shuffle

class Rack:

	def __init__(self):
		self.rack =[]
		self.numOfTiles = 0

	def isEmpty(self):
		return self.numOfTiles == 0

	def showRack(self):

		print "Current Rack"
		print "-------------"
		if(len(self.rack) == 0):
			print "Empty rack"
		else:
			print "Letter:\t",
			for x in self.rack:
				if x.letter == " ": print "blank tile",
				else: print x.letter,
			print "\nScore:\t",
			for x in self.rack:
				if x.value == -1: print "_",
				else: print x.value,
			print 

	def replenish(self,bag):

		shuffle(bag)
		needed = 7 - self.numOfTiles
		letters = bag[:needed]

		self.numOfTiles = self.numOfTiles + len(letters)

		for letter in letters:
			self.rack.append(Tile(letter))

		return bag[needed:]

	def removeTile(self,idx):
		del self.rack[idx]
		self.numOfTiles -= 1 

	def clearRack(self):
		del self.rack[:]
		self.numOfTiles = 0

	def addTile(self, tile):
		self.rack.append(tile)
		self.numOfTiles += 1


