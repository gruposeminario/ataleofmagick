#!/usr/bin/env python
# encoding: utf-8
"""
character.py

Created by C on 2009-07-11.
"""

import pygame
from pygame.locals import *
from util import load_sprite

class Character(pygame.sprite.DirtySprite):
  
  def __init__(self, screen, start_pos):
    pygame.sprite.DirtySprite.__init__(self)
    self.screen = screen
    self.sprite = load_sprite("megaman2.png")
    self.width = 28
    self.height = 30
    self.stop = True
    self.move_keys = []
    self.direction = "down"
    self.frame = 0
    self.animcounter = 0
    self.movementspeed = 2
    self.x = start_pos[0]
    self.y = start_pos[1]
    self.north = self.sprite.images([
          (0,  0, self.width, self.height),
          (28, 0, self.width, self.height),
          (56, 0, self.width, self.height)
      ], -1
    )
    self.south = self.sprite.images([
          (0,  64, self.width, self.height),
          (28, 64, self.width, self.height),
          (56, 64, self.width, self.height)
      ], -1
    )
    self.east = self.sprite.images([
          (0,  32, self.width, self.height),
          (28, 32, self.width, self.height),
          (56, 32, self.width, self.height)
      ], -1
    )
    self.west = self.sprite.images([
          (0,  96, self.width, self.height),
          (28, 96, self.width, self.height),
          (56, 96, self.width, self.height)
      ], -1
    )
    self.walking = {
          'up': self.north,
          'down': self.south,
          'right': self.east,
          'left': self.west
    }
    self.draw()
  
  def get_movement_coord(self):
    """docstring for get_movement_coord"""
    if self.direction == "up":
      self.y = self.y - self.movementspeed
    if self.direction == "down":
      self.y = self.y + self.movementspeed
    if self.direction == "right":
      self.x = self.x + self.movementspeed
    if self.direction == "left":
      self.x = self.x - self.movementspeed
    return ( self.x, self.y )
  
  def draw(self):
    """docstring for draw"""
    self.screen.fill(pygame.Color('black'))
    self.position = self.get_movement_coord()
    self.screen.blit(load_tile('terrain_forest'), 0, 0)
    self.screen.blit(self.walking[self.direction][self.frame], self.position)
    pygame.display.flip()
  
  
  def update(self):
    self.animspeed = 4
    if not self.stop:
     self.animcounter = (self.animcounter + 1) % self.animspeed
     if self.animcounter == 0:
       self.frame  = (self.frame + 1) % (len(self.walking[self.direction]))
     self.draw()
    else:
     self.frame = 0
     self.dirty = 1


      



