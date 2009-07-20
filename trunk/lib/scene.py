#!/usr/bin/env python
# encoding: utf-8
"""
game.py

Created by C on 2009-07-11.
"""

from os import environ
import pygame
from pygame.locals import * 
from character import Character
from maptool  import Map

class Scene(object):

  def __init__(self, screen):
    self.screen = screen

class WorldScene(Scene):

  def __init__(self, screen):
    Scene.__init__(self, screen)
    self.character_list = []
    self.world_map      = []

  """ Add a character to the scene """
  def addCharacter(self, character):
    self.character_list.append(character)

  """ Remove a character from the scene """
  def removeCharacter(self, character):
    self.character_list.remove(character)

  """ Set the map for the scene """
  def setMap(self, screen_dimensions, tile_dimensions, mapname):
    currentMap      = Map(screen_dimensions, tile_dimensions, mapname) 
    self.world_map  = currentMap.update()
    
  """ Update the display """
  def update(self):
   self.Characters  = pygame.sprite.Group(self.character_list)
   self.Map         = pygame.sprite.Group([self.world_map])

   """ Create layers to update """
   self.DirtyLayers = pygame.sprite.LayeredDirty()
   self.DirtyLayers.add(self.Map)
   self.DirtyLayers.add(self.Characters)
   self.DirtyLayers.update()
   rectList = self.DirtyLayers.draw(self.screen)
   pygame.display.update(rectList)

class BattleScene(Scene):
  pass
