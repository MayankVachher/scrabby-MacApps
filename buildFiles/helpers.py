import pygame, time
from gen_board import *
from tile import *
from rack import *
from trie import *
from inputbox import *

def renderWord(wordPlayed, sanitizedPosition, boardRectangles, playHorizontal, BOARD, ourBoard):
	pos_r = sanitizedPosition[1]
	pos_c = sanitizedPosition[0]

	wordPlayed = wordPlayed.upper()
	print pos_r, pos_c
	print len(wordPlayed)

	if(playHorizontal):
		for idx, x in enumerate(wordPlayed):
			renderTile(x, boardRectangles[pos_c + idx][pos_r], BOARD)
	else:
		for idx, x in enumerate(wordPlayed):
			renderTile(x, boardRectangles[pos_c][pos_r + idx ], BOARD)
	return True

def renderTile(letter2play, square, BOARD):
	FONTSMALL = pygame.font.SysFont('Andale Mono', 13)
	FONTSMALL2 = pygame.font.SysFont('Andale Mono', 8)
	square = pygame.draw.rect(BOARD, (238, 228, 218), (square.topleft[0], square.topleft[1], square.width, square.height))
	BOARD.blit(FONTSMALL.render(letter2play, 1, (50,50,50)),(square.topleft[0]+10, square.topleft[1]+5))
	BOARD.blit(FONTSMALL2.render(str(Tile(letter2play).getVal()), 1, (50,50,50)),(square.topleft[0]+17, square.topleft[1]+15))

def renderRackTile(letter, score, square, SECONDHALF):
	FONTSMALL = pygame.font.SysFont('Andale Mono', 27)
	FONTSMALL2 = pygame.font.SysFont('Andale Mono', 11)
	square = pygame.draw.rect(SECONDHALF, (238, 228, 218), (square.topleft[0], square.topleft[1], square.width, square.height))
	SECONDHALF.blit(FONTSMALL.render(letter, 1, (50,50,50)),(square.topleft[0]+9, square.topleft[1]+5))
	SECONDHALF.blit(FONTSMALL2.render(str(score), 1, (50,50,50)),(square.bottomright[0] - 15, square.bottomright[1] - 17))

def sanitizePosition(pos):
	if(len(pos) > 4): return False
	if(not pos[0].isalpha()):
		if(not pos[-1].isalpha()): return False
		x = ord(pos[-1]) - ord('A')
		pos = pos[:-1]
		pos.strip(" ")
		y = int(''.join(pos)) - 1
		if(x < 15 and x >= 0 and y < 15 and y >= 0):
			return (x,y)
		else: return False
	else:
		if(pos[-1].isalpha()): return False
		x = ord(pos[0]) - ord('A')
		pos = pos[1:]
		pos.strip(" ")
		y = int(''.join(pos)) - 1
		if(x < 15 and x >= 0 and y < 15 and y >= 0):
			return (x,y)
		else: return False

def displayScores(scorePlayer, scoreComputer, inBag, SECONDHALF, SCREEN, PLAYER_MOVE, playerTag = "Player", computerTag = "Computer"):
	
	pygame.draw.rect(SECONDHALF, (42,42,42), (0,0,500,125))
	print playerTag+" Score: "+str(scorePlayer)
	print computerTag+" Score: "+str(scoreComputer)+"\n\n"

	FONT = pygame.font.SysFont('Futura', 27)
	FONT2 = pygame.font.SysFont('Futura', 24)
	humanColor = (175,175,175)
	computerColor = (175,175,175)
	
	if(PLAYER_MOVE): humanColor = (102, 204, 255)
	else: computerColor = (102, 204, 255)

	SECONDHALF.blit(FONT.render(playerTag.upper()+":", 1, humanColor), (30, 20))
	SECONDHALF.blit(FONT.render(str(scorePlayer), 1, (175,175,175)), (210, 20))
	SECONDHALF.blit(FONT.render(computerTag.upper()+":", 1, computerColor), (30, 60))
	SECONDHALF.blit(FONT.render(str(scoreComputer), 1, (175,175,175)), (210, 60))
	SECONDHALF.blit(FONT2.render("IN BAG", 1, (204, 102, 255)), (340, 20))
	SECONDHALF.blit(FONT2.render(str(inBag), 1, (175, 175, 175)), (370, 60))
	SCREEN.blit(SECONDHALF,(500,0))
	pygame.display.flip()

def displayRack(rack, SECONDHALF, SCREEN):
	pygame.draw.rect(SECONDHALF, (42,42,42), (0,125,500,125))
	FONT = pygame.font.SysFont('Futura', 27)
	rackSquares = []
	for x in range(7):
		rackSquares.append(pygame.draw.rect(SECONDHALF, (238, 228, 218), (70+(50*x), 155, 40, 40)))
	for idx,element in enumerate(rack.rack):
		if element.letter == " ": pass
		else: renderRackTile(element.letter.upper(), element.value, rackSquares[idx], SECONDHALF)
	SECONDHALF.blit(FONT.render("YOUR RACK", 1, (204, 102, 255)), (170, 200))
	SCREEN.blit(SECONDHALF,(500,0))
	pygame.display.flip()

def generateWordList():

	#------------------------------------------
	#Build Trie

	wordListTrie = Trie()

	inputFile = open('Lexicon.txt','r')

	for word in inputFile:

		dontAdd = False

		#Check if input is sanitized
		#Don't allow anything other than lowercase English letters and EOW({)
		for item in word.strip():
			if(ord(item) > 123 or ord(item) < 97):
				dontAdd = True
		#If everything is okay		
		if not dontAdd:
			wordListTrie.addWord(word.strip())
	return wordListTrie

def verifyShuffle(shuffleLetters, playerRack):
	tiles = ''.join([t.letter.upper() for t in playerRack.rack])
	tiles = dict((c, tiles.count(c)) for c in tiles)
	shuffled = dict((c, shuffleLetters.count(c)) for c in shuffleLetters)

	for x in shuffled.keys():
		if(x not in tiles.keys()):
			return False
		else:
			if(shuffled[x] > tiles[x]): return False
	return True


def getDetails(SECONDHALF, SCREEN, wordListTrie, playerRack):
	FONT = pygame.font.SysFont('Andale Mono', 22)

	playerRack.showRack()

	shuffle = ask(SCREEN, SECONDHALF, "SHUFFLE? (YES/NO)")
	if(len(shuffle) != 0): shuffle = shuffle.upper()[0]
	if(shuffle == 'Y' or shuffle == 'N'):
		if(shuffle == 'Y'):
			shuffle = True

			shuffleLetters = ask(SCREEN, SECONDHALF, "LETTERS:")
			if(verifyShuffle(shuffleLetters, playerRack)):
				return ("Shuffle", shuffleLetters.lower())

			else:
				print "Shuffle-Letters: INCORRECT"
				SECONDHALF.blit(FONT.render("INCORRECT LETTERS! TRY AGAIN!", 1, (255,0,0)), ((SECONDHALF.get_width() / 2) - 200, (SECONDHALF.get_height() / 2) + 170))
				SCREEN.blit(SECONDHALF, (500,0))
				pygame.display.flip()
				time.sleep(3)
				return False
		
		else:
			shuffle = False

			wordPlayed = ask(SCREEN, SECONDHALF, "WORD?")
			if(wordListTrie.query(wordPlayed.lower())): #Check if legit word
				print "Word? " + wordPlayed
				
				positionPlayed = ask(SCREEN, SECONDHALF, "POSITION? (ROW COL)")
				sanitizedPos = sanitizePosition(positionPlayed)
				if(sanitizedPos != False): #Check if legit position
					print "Position? " + positionPlayed
					print "After Sanitization: "+str(sanitizedPos)

					playHorizontal = ask(SCREEN, SECONDHALF, "ACROSS? (YES/NO)")
					playHorizontal = (playHorizontal).upper()
					if(playHorizontal != "YES" and playHorizontal != "NO" and playHorizontal != "Y" and playHorizontal != "N"):
						print "Across? WEIRD INPUT"
						SECONDHALF.blit(FONT.render("WEIRD INPUT! TRY AGAIN!", 1, (255,0,0)), ((SECONDHALF.get_width() / 2) - 200, (SECONDHALF.get_height() / 2) + 170))
						SCREEN.blit(SECONDHALF, (500,0))
						pygame.display.flip()
						time.sleep(3)
						return False
			
					else:
						playHorizontal = playHorizontal[0]
						if playHorizontal == 'Y': print "Horizontal? Y"; playHorizontal = True
						else: print "Horizontal? N"; playHorizontal = False
						return ("Move", wordPlayed.lower(), sanitizedPos, playHorizontal)
				else:
					print "Position? " + positionPlayed + " - Invalid Position!"
					SECONDHALF.blit(FONT.render("Invalid Position! TRY AGAIN!", 1, (255,0,0)), ((SECONDHALF.get_width() / 2) - 200, (SECONDHALF.get_height() / 2) + 170))
					SCREEN.blit(SECONDHALF, (500,0))
					pygame.display.flip()
					time.sleep(3)
					return False
			else:
				print "Word? " + wordPlayed + " - This word does not exist!"
				SECONDHALF.blit(FONT.render("Word is Non-existent! TRY AGAIN!", 1, (255,0,0)), ((SECONDHALF.get_width() / 2) - 200, (SECONDHALF.get_height() / 2) + 170))
				SCREEN.blit(SECONDHALF, (500,0))
				pygame.display.flip()
				time.sleep(3)
				return False
	else:
		print "Shuffle? WEIRD INPUT"
		SECONDHALF.blit(FONT.render("WEIRD INPUT! TRY AGAIN!", 1, (255,0,0)), ((SECONDHALF.get_width() / 2) - 200, (SECONDHALF.get_height() / 2) + 170))
		SCREEN.blit(SECONDHALF, (500,0))
		pygame.display.flip()
		time.sleep(3)
		return False		

def removeTiles(playerRack, letters):
	#print letters
	for x in letters:
		tiles = [t.letter for t in playerRack.rack]
		for idx, elem in enumerate(tiles):
			if(tiles[idx] == x):
				#print "Found "+x+" and deleting it"
				playerRack.removeTile(idx)
				break
	#playerRack.showRack()
	return playerRack