#!/usr/bin/env python
# encoding: utf-8
"""
character.py

Created by C on 2009-07-11.
"""
import ConfigParser, os
import pygame
from pygame.locals import *
from util import load_character

# Resource loading:
DATA_PY = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.normpath(os.path.join(DATA_PY, '..', 'data/characters/')) 

""" A generic character class for a sprite based character """
class Character(pygame.sprite.DirtySprite):
  
  def __init__(self, name):
    pygame.sprite.DirtySprite.__init__(self)
    self.name = name
    """ Parse Data from Character's Config File """ 
    self.character_config = ConfigParser.RawConfigParser()
    self.character_config.read(os.path.join(DATA_DIR, self.name + ".ini"))
    self.__parsedata()

    self.stats = {}
    self.__parsestats()

    """ Set positional images """
    self.north = self.sprite.images([
          (self.image_start_x,                     self.image_start_y, self.width, self.height),
          (self.image_start_x + self.width,        self.image_start_y, self.width, self.height),
          (self.image_start_x + (self.width * 2),  self.image_start_y, self.width, self.height)
      ], -1
    )
    self.east = self.sprite.images([
          (self.image_start_x,                     self.height, self.width, self.height),
          (self.image_start_x + self.width,        self.height, self.width, self.height),
          (self.image_start_x + (self.width * 2),  self.height, self.width, self.height)
      ], -1
    )
    self.south = self.sprite.images([
          (self.image_start_x,                     (self.height * 2), self.width, self.height),
          (self.image_start_x + self.width,        (self.height * 2), self.width, self.height),
          (self.image_start_x + (self.width * 2),  (self.height * 2), self.width, self.height)
      ], -1
    )
    self.west = self.sprite.images([
          (self.image_start_x,                     (self.height * 3), self.width, self.height),
          (self.image_start_x + self.width,        (self.height * 3), self.width, self.height),
          (self.image_start_x + (self.width * 2),  (self.height * 3), self.width, self.height)
      ], -1
    )
    self.walking = {
          'up': self.north,
          'down': self.south,
          'right': self.east,
          'left': self.west
    }
    self.image = self.walking[self.direction][self.frame]
    self.rect = self.image.get_rect(left=self.x, top=self.y)
    self.collide_surface = pygame.Surface((11,6))
    self.collide_rect = self.collide_surface.get_rect(
        left=self.rect.left + 11, bottom=self.rect.bottom)

  def getStat(self, stat):
    return self.stats[stat]

  def setStat(self, stat, value):
    self.stats[stat] = value

  def __parsestats(self):
    self.stats['vitality'] = self.character_config.getint("stats", "vitality")

  def __parsedata(self):
    
    self.sprite                             = load_character(self.character_config.get("config", "file_name"))
    self.width, self.height                 = self.character_config.getint("config", "width"), self.character_config.getint("config", "height")
    self.x, self.y                          = self.character_config.getint("config", "start_x"), self.character_config.getint("config", "start_y")
    self.image_start_x, self.image_start_y  = self.character_config.getint("image", "start_x"), self.character_config.getint("image", "start_y")
    self.movementspeed                      = self.character_config.getint("config", "movement_speed")
    self.frame                              = self.character_config.getint("config", "start_frame")
    self.direction                          = self.character_config.get("config", "direction")

    """ Non config file related settings """
    self.stop = True
    self.move_keys = []
    self.animcounter = 0
  
  def get_movement_coord(self):
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
    self.animcounter = (self.animcounter + 1) % self.animspeed
    if self.animcounter == 0:
      self.frame  = (self.frame + 1) % (len(self.walking[self.direction]))
    self.position = self.get_movement_coord()
    self.image = self.walking[self.direction][self.frame]
    self.rect = self.image.get_rect(left=self.x, top=self.y)

  def move_check(self):
    pass
  
  def update(self):
    self.animspeed = 4
    if not self.stop:
     self.move_check()
     self.draw()
    else:
     self.frame = 0
     self.dirty = 1


      



