#!/usr/bin/env python
# encoding: utf-8
"""
scroll.py

Created by C on 2009-07-11.

[TEST CASE]

Objective:

This file is to test the effects of the rectangle
and surface interaction of pygame

Basically what we will be doing is taking a huge bmp image and using the arrow
keys to scroll the view

create a surface to store the large bitmap
get the rectangle coordinates of the large image


"""
import sys
import os
import pygame
from pygame.locals import *

MOVING = False
MOVEMENT_SPEED = 10
X = 0
Y = 0

pygame.init()
screen  = pygame.display.set_mode((800, 600))
image   = pygame.image.load(os.path.join("megamanbeads.jpg")).convert_alpha()
screen.blit(image, (0,0))
rect    = image.get_rect()
pygame.time.Clock().tick(30)
if pygame.image.get_extended():
  print "JPG LOADED"

pygame.display.update()

def move_camera(screen, offset):
  print offset
  screen.blit(image, offset)
  pygame.display.flip()

while 1:
  for event in pygame.event.get():
    if event.type == QUIT:
      sys.exit()
    elif event.type == KEYDOWN:
      if event.key == K_ESCAPE:
        sys.exit()
      elif event.key in(K_DOWN, K_UP, K_LEFT, K_RIGHT):
        """MOVE CAMERA"""
        CURRENT_KEY = event.key
        MOVING = True
      
    elif event.type == KEYUP:
      if event.key in(K_DOWN, K_UP, K_LEFT, K_RIGHT):
       """STOP MOVING CAMERA"""
       MOVING = False

  if MOVING == True:
    print X
    if CURRENT_KEY == K_LEFT:
      if X < 0:
        X = X + MOVEMENT_SPEED
    if CURRENT_KEY == K_RIGHT:
      if X > -1470:
        X = X - MOVEMENT_SPEED
    if CURRENT_KEY == K_DOWN:
      if Y > -950:
        Y = Y - MOVEMENT_SPEED
    if CURRENT_KEY == K_UP:
      if Y < 0:
        Y = Y + MOVEMENT_SPEED
    move_camera(screen, (X,Y))


