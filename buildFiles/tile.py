class Tile:

	def __init__(self, l = '_'):
		self.letter = l.lower()
		self.value = self.setVal(l)

	def getVal(self):
		return self.value

	def setVal(self, l):
		if l in "_": return -1
		if l in " ": return 0
		if l in "aeilnorstuAEILNORSTU": return 1
		if l in "dgDG": return 2
		if l in "bcmpBCMP": return 3
		if l in "fhvwyFHVWY": return 4
		if l in "kK": return 5
		if l in "jxJX": return 8
		if l in "qzQZ": return 10