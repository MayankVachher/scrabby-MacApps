# by Timothy Downs, inputbox written for my map editor

# This program needs a little cleaning up
# It ignores the shift key
# And, for reasons of my own, this program converts "-" to "_"

# A program to get user input, allowing backspace etc
# shown in a box in the middle of the screen
# Called by:
# import inputbox
# answer = inputbox.ask(screen, "Your name")
#
# Only near the center of the screen is blitted to

import pygame, pygame.font, pygame.event, pygame.draw, string, sys
from pygame.locals import *

def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == pygame.QUIT: sys.exit()
    elif event.type == KEYDOWN:
      return event.key
    else:
      pass

def display_box(lvl2, screen, message, color):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.SysFont('Andale Mono', 30)
  pygame.draw.rect(screen, color,
                   (0, (screen.get_height() / 2),
                    screen.get_width(),(screen.get_height() / 2)), 0)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (255,255,255)),
                ((screen.get_width() / 2) - 150, (screen.get_height() / 2) + 100))
    lvl2.blit(screen, (500,0))
  pygame.display.flip()

def display_box2(lvl2, screen, message, ques):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.SysFont('Andale Mono', 22)
  fontobject2 = pygame.font.SysFont('Andale Mono', 30)
  pygame.draw.rect(screen, (25,25,25),
                   (0, (screen.get_height() / 2),
                    screen.get_width(),(screen.get_height() / 2)), 0)
  if len(ques) != 0:
    screen.blit(fontobject2.render(ques.upper(), 1, (255,255,255)),
                ((screen.get_width() / 2) - 200, (screen.get_height() / 2) + 30))
  if len(message) != 0:
    screen.blit(fontobject.render(message.upper(), 1, (255,255,255)),
                ((screen.get_width() / 2) - 200, (screen.get_height() / 2) + 70))
  lvl2.blit(screen, (500,0))
  pygame.display.flip()

def ask(lvl2, screen, question):
  "ask(screen, question) -> answer"
  #pygame.font.init()
  current_string = []
  display_box2(lvl2, screen, "", question)
  while 1:
    inkey = get_key()
    if inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == K_RETURN:
      break
    elif inkey == K_MINUS:
      current_string.append("_")
    elif inkey <= 127:
      current_string.append(chr(inkey))
    display_box2(lvl2, screen, string.join(current_string,""), question)
  return string.join(current_string,"").upper()

def main():
  screen = pygame.display.set_mode((320,240))
  #print ask(screen, "Name") + " was entered"

if __name__ == '__main__': main()