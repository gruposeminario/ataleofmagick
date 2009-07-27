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

""" Global Config """
from globals import *

# Resource loading:
DATA_PY = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.normpath(os.path.join(DATA_PY, '..', 'data/characters/')) 

""" A generic character class for a sprite based character """
class Character(pygame.sprite.DirtySprite):
  
  def __init__(self, name, collidelist):
    pygame.sprite.DirtySprite.__init__(self)
    self.name = name
    self.collidelist = collidelist
    self.camera_moving = {
      "up"    : False,
      "down"  : False,
      "right" : False,
      "left"  : False
    }
    """ Parse Data from Character's Config File """ 
    self.character_config = ConfigParser.RawConfigParser()
    self.character_config.read(os.path.join(DATA_DIR, self.name + ".ini"))
    self.stats = {}
    self.__parsedata()


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
          'up'    : self.north,
          'down'  : self.south,
          'right' : self.east,
          'left'  : self.west
    }

    """ Set sprite's images"""
    self.image = self.walking[self.direction][self.frame]
    self.rect = self.image.get_rect(left=self.x, top=self.y)

    """ Collide Rectangle """
    self.collide_surface = pygame.Surface((self.width, self.height))
    self.collide_rect = self.collide_surface.get_rect(left=self.x, top=self.y)

    """ Camera Rectangle """
    self.camera_surface = pygame.Surface((self.width+G["camera_width"], self.height+G["camera_height"]))
    self.camera_rect    = self.camera_surface.get_rect(center=(self.x+self.width,self.y+self.height))

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
    
    """ Parse character stats """
    self.__parsestats()

    """ Non config file related settings """
    self.stop = True
    self.move_keys = []
    self.animcounter = 0
    self.collision = {}
    self.edge_collision = {}

  """ Return the Camera View of the Sprite """
  def getCamera(self):
    return self.camera_rect

  def update_movement_coord(self):
    x, y = self.x, self.y
    """ Check for the Camera """
    if self.camera_moving[self.direction] == True:
      return (x, y)
    if self.direction == "up":
      y = self.y - self.movementspeed
    if self.direction == "down":
      y = self.y + self.movementspeed
    if self.direction == "right":
      x = self.x + self.movementspeed
    if self.direction == "left":
      x = self.x - self.movementspeed
    return (x, y)

  """ Draw character sprite """
  def draw(self):
    if self.collision[self.direction] == False and self.edge_collision[self.direction] == False:
      self.animcounter = (self.animcounter + 1) % self.animspeed
      if self.animcounter == 0:
        self.frame  = (self.frame + 1) % (len(self.walking[self.direction]))
      coords            = self.update_movement_coord()
      self.x, self.y    = coords[0], coords[1]
      self.image        = self.walking[self.direction][self.frame]
      """ Update Hero Rect """
      self.rect         = self.image.get_rect(left=self.x, top=self.y)
      """ Update collision rectangle """
      self.collide_rect = self.collide_surface.get_rect(left=self.x, top=self.y)
      """ Update the camera's rectangle """
      self.camera_rect    = self.camera_surface.get_rect(center=(self.x+self.width,self.y+self.height))

  """ Not sure what the needs are for moving a npc yet """
  def stop_move(self):
    self.stop   = True
    self.frame  = 0
    self.dirty  = 1

  def update(self):
    self.animspeed = 4
    if not self.stop:
     self.move_check()
     self.draw()
    else:
     self.stop_move()
      
  """ Need to check preemptively for direction that the rect will move to """
  def move_check(self):
    directions = {
        'up': self.collide_rect.move(0,-self.movementspeed),
        'down': self.collide_rect.move(0,self.movementspeed),
        'left': self.collide_rect.move(-self.movementspeed,0),
        'right': self.collide_rect.move(self.movementspeed,0) 
    }
    for direction, rect in directions.iteritems():
      self.check_edge(direction, rect)
      self.check_collide_npc(direction, rect)

  def check_edge(self, direction, rect):
    sprite_left   = rect.midleft[0]
    sprite_right  = rect.midright[0]
    sprite_top    = rect.midtop[1]
    sprite_bottom = rect.midbottom[1]

    if sprite_left <= 0 or sprite_top <= 0 or sprite_right >= (G["screen_width"] - 10) or sprite_bottom >= (G["screen_height"] - 10):
      self.image = self.walking[self.direction][self.frame]
      self.edge_collision[direction] = True
      if self.edge_collision[self.direction] == True:
        self.stop_move()
    else:
      self.edge_collision[direction] = False

  """ Check Collisions against NPC Objects """
  def check_collide_npc(self, direction, rect):
    if rect.collidelistall(self.collidelist) != []:
      """ Face object if a collision is found but don't move """
      self.image = self.walking[direction][self.frame]
      self.collision[direction] = True
      if self.collision[self.direction] == True:
        self.stop_move()
    else:
      self.collision[direction] = False

""" Define a Hero (Player) Character """
""" Migrate to a Hero Class """
class Hero(Character):
  def __init__(self, name, collidelist):
    Character.__init__(self, name, collidelist)
