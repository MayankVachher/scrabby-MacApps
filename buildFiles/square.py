from tile import *

class Square:

	#tile = Tile() # The tile that is on the square
	#occupied = False # Whether the square is occupied or not
	#isAnchor = False # Whether the square is an anchor square or not
	#crossCheck = [] # Something that Anmol needed
	""" 0 - Nothing Special, 1 - Double Letter(DL), 2 - Triple Letter(TL), 3 - Double Word(DW), 4 - Triple Word(TW) """
	#special = 0 # The type of square it is

	def __init__(self):
		self.occupied = False
		self.isAnchor = False
		self.downCrossCheck = []
		self.acrossCrossCheck = []
		self.downCrossSum = 0
		self.acrossCrossSum = 0
		for _ in range(26):
			self.downCrossCheck.append(True) #If true for a letter, then it is safe to play that letter on this square in a down move. 
		for _ in range(26):
			self.acrossCrossCheck.append(True) #If true for a letter, then it is safe to play that letter on this square in an across move.
		self.special = 0
		self.tile = Tile()

	def changeSpeciality(self,val): # Change the type of the square
		self.special = val

	def setTile(self,val): # Place a tile on the square
		self.tile = val
		self.occupied = True

	def setTileVal(self, val):
		self.tile = val

	def getChar(self):
		return self.tile.letter



def main():
	pass

if __name__ == '__main__':
	main()