import sys, pygame, time, datetime
import numpy as np
from gen_board import *
from tile import *
from rack import *
from trie import *
from inputbox import *
from helpers import *
from game import *
from copy import deepcopy
from collections import OrderedDict
import random

allLetters = "eeeeeeeeeeeeaaaaaaaaaiiiiiiiiioooooooonnnnnnrrrrrrttttttllllssssuuuuddddgggbbccmmppffhhvvwwyykjxqz"
isRandomWalk = 0
canGoHomeNow = 0

leaves = { 'A' : -0.63, 'B' : -2.00, 'C' : 0.8, 'D': 0.45, 'E' :0.35, 'F': -2.21, 'S' :8.04,'Z' :5.12,'X' :3.31,'R' :1.10,'H' :1.09,'M' :0.58,'N' :0.22,'T' :-0.10,'L' :-0.17,'P' :-0.46,'K' :-0.54,'Y' :-0.63,'J' :-1.47,'I' :-2.07,'O' :-2.50,'G' :-2.85,'W' :-3.82,'U' :-5.10,'V' :-5.55, 'Q' :-6.79 }

def run_game():

	#------------------------------------------
	#Init Board
	
	ourBoard = TheBoard()

	scorePlayer = 0
	scoreComputer = 0

	playerRack = Rack()
	computerRack = Rack()

	bag = [ letter for letter in allLetters ]

	bag = playerRack.replenish(bag)
	bag = computerRack.replenish(bag)

	playerTurn = True
	#playerTurn = False

	wordListTrie = generateWordList()

	#------------------------------------------
	#Pygame starts

	pygame.init()
	size = width, height = 1000, 500

	#------------------------------------------
	#Screen Setup

	WINDOW = pygame.display.set_mode(size)
	CAPTION = pygame.display.set_caption('Scrabby')
	SCREEN = pygame.display.get_surface()
	SCREEN.fill((150, 141, 131))
	FIRSTHALF = pygame.Surface((size[0]/2, size[1]))
	FIRSTHALF.fill((51, 51, 51))
	SECONDHALF = pygame.Surface((size[0]/2, size[1]))
	SECONDHALF.fill((42, 42, 42))
	BOARD = pygame.Surface((462, 462))
	BOARD.fill((10, 10, 10))
	TRANSPARENT = pygame.Surface(size)
	TRANSPARENT.set_alpha(255)
	TRANSPARENT.fill((255,255,255))

	#------------------------------------------
	#Fonts Setup

	FONTSMALL = pygame.font.SysFont('Futura', 15)
	FONTSMALL2 = pygame.font.SysFont('Andale Mono', 13)

	#------------------------------------------
	#Board Setup

	boardRectangles = []
	rowMarkers = []
	colMarkers = []
	for x in range(0, 463, 29):
		rowRectangles = []
		for y in range(0, 463, 29):
			if(y == 435):
				if(x == 435): rect = pygame.draw.rect(BOARD, (238, 228, 218), (x,y,29,29))
				else: rect = pygame.draw.rect(BOARD, (238, 228, 218), (x,y,27,29))
			elif(x == 435): rect = pygame.draw.rect(BOARD, (238, 228, 218), (x,y,29,27))
			else: rect = pygame.draw.rect(BOARD, (238, 228, 218), (x,y,27,27))
			
			if(y == 0): colMarkers.append(rect)
			elif(x == 0): rowMarkers.append(rect)
			else: rowRectangles.append(rect)
		
		if(len(rowRectangles) != 0): boardRectangles.append(rowRectangles)

	#Beautify the Board
	for idx, x in enumerate(ourBoard.board):
		for idy, y in enumerate(x):
			myRect = boardRectangles[idx][idy]
			if y.occupied == True: pass #print boardRectangles[idx][idy]
			else:
				if y.special == 4: specialColor = (255, 0, 0) #TW
				elif y.special == 3: specialColor = (255, 153, 255) #DW
				elif y.special == 2: specialColor = (0, 102, 255) #TL
				elif y.special == 1: specialColor = (102, 204, 255) #DL
				else: specialColor = (84, 130, 53)
				myRect = pygame.draw.rect(BOARD, specialColor, (myRect.topleft[0],myRect.topleft[1], myRect.width, myRect.height))
				if y.special == 4: BOARD.blit(FONTSMALL2.render("TW", 1, (50,50,50)),(myRect.topleft[0]+5, myRect.topleft[1]+5))
				elif y.special == 3: BOARD.blit(FONTSMALL2.render("DW", 1, (50,50,50)),(myRect.topleft[0]+5, myRect.topleft[1]+5))
				elif y.special == 2: BOARD.blit(FONTSMALL2.render("TL", 1, (50,50,50)),(myRect.topleft[0]+5, myRect.topleft[1]+5))
				elif y.special == 1: BOARD.blit(FONTSMALL2.render("DL", 1, (50,50,50)),(myRect.topleft[0]+5, myRect.topleft[1]+5))

	#########################################
	#Row-Column Markers are rendered next

	mychar = 'A'

	for idx, x in enumerate(colMarkers):
		if(idx == 0): x = pygame.draw.rect(BOARD, (51, 51, 51), (x.topleft[0], x.topleft[1], x.width+2, x.height+2))
		else:
			x = pygame.draw.rect(BOARD, (51, 51, 51), (x.topleft[0], x.topleft[1], x.width+2, x.height))
			BOARD.blit(FONTSMALL.render(mychar, 1, (200,200,200)),(x.topleft[0]+10, x.topleft[1]+5))
			mychar = chr(ord(mychar) + 1)

	mynum = 1

	for idx, x in enumerate(rowMarkers):
		x = pygame.draw.rect(BOARD, (51, 51, 51), (x.topleft[0], x.topleft[1], x.width, x.height+2))
		BOARD.blit(FONTSMALL.render(str(mynum), 1, (200,200,200)),(x.topleft[0]+5, x.topleft[1]+5))
		mynum += 1


	#-----------------------------------------
	#Refresh Display

	FIRSTHALF.blit(BOARD, (19,19))
	SCREEN.blit(FIRSTHALF,(0,0))
	SCREEN.blit(SECONDHALF,(500,0))
	displayScores(scorePlayer, scoreComputer, len(bag), SECONDHALF, SCREEN, playerTurn)
	displayRack(playerRack, SECONDHALF, SCREEN)
	pygame.display.flip()


	#-----------------------------------------

	ourBoard.printBoard()
	print "Player gets to move first!\n"

	#-----------------------------------------
	#Main Loop

	firstMoveFlag = True
	scoringTimes = []
	crossTimes = []
	genTimes = []
	moveTimes = []
	simTimes = []

	while True and not (playerRack.isEmpty() or computerRack.isEmpty()):

		
		#------------------------------------
		#Detect Events

		if(firstMoveFlag):
			ourBoard.board[7][7].isAnchor = True
			firstMoveFlag = False

		if(playerTurn):

			setCrossCheckBits(ourBoard, wordListTrie)

			motion = getDetails(SECONDHALF, SCREEN, wordListTrie, playerRack) #Get Info from Player
			if(motion == False): #If Info is not legit, continue
				continue
			elif(motion[0] == "Shuffle"): #If Users asks for shuffle
				if(len(bag) == 0):
					if(canGoHomeNow == 1):
						print "Human: Can't possibly find a move.\nEnding Game.\nGGWP All.\n"
						break
					else:
						canGoHomeNow = 1
				print motion[1]
				playerRack = removeTiles(playerRack, motion[1])
				print "Shuffle Success!\n\n"
				playerTurn = False
				bag = playerRack.replenish(bag) #Replenish Player's Rack after shuffle
				displayRack(playerRack, SECONDHALF, SCREEN) #Display Player's New Rack
				playerRack.showRack()

				bag += [x for x in motion[1]]
				display_box(SCREEN, SECONDHALF, "SHUFFLE SUCCESS!", (107,142,35))
				time.sleep(2)
				displayScores(scorePlayer, scoreComputer, len(bag), SECONDHALF, SCREEN, playerTurn) #Display Scores

			else: #If Info is legit, try playing the word
				#Check for valid move here
				current = validityCheck(motion[3], ourBoard, motion[2], motion[1], playerRack)

				if not (current):
					print "Error. Invalid Move.\n\n"
					display_box(SCREEN, SECONDHALF, "Invalid Move!", (139,0,0))
					time.sleep(2)
					continue
				else:
					renderWord(motion[1], motion[2], boardRectangles, motion[3], BOARD, ourBoard)
					FIRSTHALF.blit(BOARD, (19,19))
					SCREEN.blit(FIRSTHALF,(0,0))
					pygame.display.flip()
					print "Move Success!\n\n"
					display_box(SCREEN, SECONDHALF, "MOVE SUCCESS!", (107,142,35))
					time.sleep(2)
					#current = motion[1]

					print "Before player move:"
					playerRack.showRack()
					playerRack = removeTiles(playerRack, current)

					#need to call scoreThisMove before playerMove function is called because the latter sets tile to occupied
					scorePlayer += scoreThisMove(ourBoard, motion[1], (motion[2][0], motion[2][1]), motion[3]) #calculate score of the move
					playerMove(ourBoard, motion[1], (motion[2][0], motion[2][1]), motion[3]) #Play the move on offline board
					
					playerTurn = False #Change turn to Computer
					bag = playerRack.replenish(bag) #Replenish Player's Rack after legit move
					displayScores(scorePlayer, scoreComputer, len(bag), SECONDHALF, SCREEN, playerTurn) #Display Scores
					displayRack(playerRack, SECONDHALF, SCREEN) #Display Player's New Rack
					print "After player move:"
					playerRack.showRack()
					ourBoard.printBoard() #DisplayBoard

					canGoHomeNow = 0

		else: #AI
			print "Computer is thinking it's move!\n\n\n"

			moveStart = datetime.datetime.now()
			crossStart = datetime.datetime.now()

			setCrossCheckBits(ourBoard, wordListTrie)

			crossEnd = datetime.datetime.now()

			crossTimes.append((crossEnd-crossStart).microseconds)

			display_box(SCREEN, SECONDHALF, "COMPUTER'S TURN!", (160,36,34))
			#time.sleep(2)


			genStart = datetime.datetime.now()

			rack = [tile.letter for tile in computerRack.rack]

			#List of 4-tuples: (word, pos, isAcross, anchorPos)			
			legalWords = []

			#Generate all across moves
			for rowIdx, row in enumerate(ourBoard.board):

				prevAnchor = -1
				for idx, sq in enumerate(row):
					if sq.isAnchor:

						limit = min(idx, idx-prevAnchor-1)
						anchorSquare = idx
						prevAnchor = anchorSquare

						leftPart(ourBoard.board, rowIdx, rack, '', wordListTrie.root, anchorSquare, limit, legalWords)

			#Generate all down moves
			for colIdx in xrange(len(ourBoard.board)):

				prevAnchor = -1
				for rowIdx in xrange(len(ourBoard.board)):
					sq = ourBoard.board[rowIdx][colIdx]
					if sq.isAnchor:

						limit = min(rowIdx, rowIdx-prevAnchor-1)
						anchorSquare = rowIdx
						prevAnchor = anchorSquare

						upperPart(ourBoard.board, colIdx, rack, '', wordListTrie.root, anchorSquare, limit, legalWords)

			genEnd = datetime.datetime.now()

			genTimes.append((genEnd-genStart).microseconds)

			
			if(len(legalWords)):

				wordsWithScores = {} #dictionary of words with their scores

				scoringStart = datetime.datetime.now()

				for i in xrange(len(legalWords)):
					currentScore = scoreThisMove(ourBoard, legalWords[i][0], legalWords[i][1], legalWords[i][2] )
					wordsWithScores[legalWords[i]] = (currentScore, currentScore + computeLeaves(legalWords[i][0], legalWords[i][1], legalWords[i][2], computerRack, ourBoard))

				wordsWithScores = OrderedDict(sorted(wordsWithScores.items(), key=lambda t: t[1][1], reverse = True)) #sorted dictionary

				i = 0
				for k in wordsWithScores: 
					legalWords[i] = k
					i += 1

				scoringEnd = datetime.datetime.now()

				timeTaken = (scoringEnd - scoringStart).microseconds
				scoringTimes.append(timeTaken)

				# print legalWords[0][0], wordsWithScores[legalWords[0]]
				# print legalWords[0][3], legalWords[0][4]
				if(isRandomWalk == 0):
					print "Greedy!"
					AIWord = legalWords[0]
				elif(isRandomWalk == 1):
					print isRandomWalk
					print "Random Walk!"
					AIWord = legalWords[random.randint(0,len(legalWords) - 1)]

				else:
					# print "Top Ten: "+str(legalWords[:10])
					# print "Top Ten: "+str([wordsWithScores[x] for x in legalWords[:10]])

					simStart = datetime.datetime.now()

					AIWord = getBestWord(ourBoard, legalWords[:5], computerRack, bag)

					simEnd = datetime.datetime.now()
					simTimes.append((simEnd-simStart).microseconds)

				current = validityCheck(AIWord[2], ourBoard, AIWord[1], AIWord[0], computerRack)

				if not current:
					print "Try again."
					continue
				else:

					renderWord(AIWord[0], AIWord[1], boardRectangles, AIWord[2], BOARD, ourBoard)
					FIRSTHALF.blit(BOARD, (19,19))
					SCREEN.blit(FIRSTHALF,(0,0))
					pygame.display.flip()
					print "Move Success!\n\n"
					display_box(SCREEN, SECONDHALF, "MOVE SUCCESS!", (107,142,35))
					time.sleep(1)

					print "Before Computer Move:"
					computerRack.showRack()

					computerRack = removeTiles(computerRack, current)

					print "\nAI played:", AIWord[:3]
					print "Score of move:", wordsWithScores[AIWord][0]
					print


					scoreComputer += wordsWithScores[AIWord][0]
					playerMove(ourBoard,AIWord[0], AIWord[1], AIWord[2])

					playerTurn = True
					#if(len(bag) == 0): playerTurn = True
					bag = computerRack.replenish(bag);

					displayScores(scorePlayer, scoreComputer, len(bag), SECONDHALF, SCREEN, playerTurn)
					print "After Computer Move:"
					computerRack.showRack()

					ourBoard.printBoard()

				canGoHomeNow = 0


			else:
				if(len(bag) == 0):
					if canGoHomeNow == 1:
						print "Computer: Can't possibly find a move.\nEnding Game.\nSigh.\nGGWP.\n"
						break
					else:
						canGoHomeNow = 1
						playerTurn = True
						print "Computer: Can't possibly find a move.\nWaiting for Human's Response.\n"
						continue
				else:
					print "No Move Possible! Had to shuffle!"
					toRemove = ''.join([x.letter for x in computerRack.rack])
					if(len(bag) < 7): toRemove = toRemove[:len(bag)]
					computerRack = removeTiles(computerRack,toRemove)
					print "Shuffle Success!\n\n"
					bag = computerRack.replenish(bag) #Replenish Player's Rack after shuffle
					bag += [x for x in toRemove]

					playerTurn = True

					display_box(SCREEN, SECONDHALF, "SHUFFLE SUCCESS!", (107,142,35))
					time.sleep(2)
					displayScores(scorePlayer, scoreComputer, len(bag), SECONDHALF, SCREEN, playerTurn) #Display Scores

				continue

			moveEnd = datetime.datetime.now()
			moveTimes.append((moveEnd - moveStart).microseconds)		

		pygame.display.flip()

	print "Stats for nerdz"
	if(len(crossTimes)):
		print "Average crosscheck time:", sum(crossTimes)/float(len(crossTimes))
		print "Std deviation:", np.std(crossTimes)
	if(len(genTimes)):
		print "Average move gen time:", sum(genTimes)/float(len(genTimes))
		print "Std deviation:", np.std(genTimes)
	if(len(scoringTimes)):
		print "Average scoring time:", sum(scoringTimes)/float(len(scoringTimes))
		print "Std deviation:", np.std(scoringTimes)
	if(len(simTimes)):
		print "Average sim time:", sum(simTimes)/float(len(simTimes))
		print "Std deviation:", np.std(simTimes)
	if(len(moveTimes)):	
		print "Average move time:", sum(moveTimes)/float(len(moveTimes))
		print "Std deviation:", np.std(moveTimes)

	if scoreComputer > scorePlayer:
		res = "COMPUTER"
		display_box(SCREEN, SECONDHALF, "COMPUTER WON!", (0, 102, 255))
	elif scorePlayer > scoreComputer:
		res = "PLAYER"
		display_box(SCREEN, SECONDHALF, "PLAYER WON!", (0, 102, 255))
	else:
		display_box(SCREEN, SECONDHALF, "TIE!", (0, 102, 255))

	#sys.exit(0)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()

def main():
	# if len(sys.argv) != 2:
	# 	print "\nUsage: python "+sys.argv[0]+" 0",
	# 	print "or python "+sys.argv[0]+" 1\n"
	# 	sys.exit(1)
	global isRandomWalk
	isRandomWalk = 0
	run_game()

if __name__ == '__main__':
	main()