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
from map import Map
from camera import Camera

""" Global Config """
from globals import *

class Scene(object):

  def __init__(self, screen):
    self.screen = screen

class WorldScene(Scene):

  def __init__(self, screen):
    Scene.__init__(self, screen)
    self.character_list = []
    self.npc_list       = []

  """ Add a character to the scene """
  def addCharacter(self, character):
    self.character_list.append(character)

  """ Remove a character from the scene """
  def removeCharacter(self, character):
    self.character_list.remove(character)

  def addNPC(self, character):
    self.npc_list.append(character)

  def removeNPC(self, character):
    self.npc_list.remove(character)

  def setHero(self, character):
    self.hero = character

  """ Set the map for the scene """
  def setMap(self, mapname):
    currentMap        = Map(mapname) 
    self.world_map    = currentMap.update()
    self.WorldCamera  = Camera(self.world_map, (0, 0), self.hero.movementspeed)
  
  """ Update the display """
  def update(self):

   """ Control the Camera """
   if self.hero.stop == False:
    self.WorldCamera.check_focus(self.hero, self.hero.movementspeed)
    self.world_map.rect = self.WorldCamera.getUpdate()
    """ Loop through the camera and see if any positions need to be stopped from the main character """
    for direction in self.WorldCamera.map_moving:
      self.character_list[0].camera_moving[direction] = self.WorldCamera.map_moving[direction]

   """ Setup the character and map layers """
   self.HeroCharacters  = pygame.sprite.Group(self.character_list)
   self.NPCCharacters   = pygame.sprite.Group(self.npc_list)
   self.Map             = pygame.sprite.Group([self.world_map])

   """ If Debug Camera is enabled show the hero's camera """
   if D["camera"] == True:
    pygame.draw.rect(self.screen, (255,255,255), self.hero.camera_rect)
    pygame.display.flip()

   """ Create layers to update """
   GameLayers = pygame.sprite.LayeredDirty()
   GameLayers.add(self.Map)
   GameLayers.add(self.HeroCharacters)
   GameLayers.add(self.NPCCharacters)
   GameLayers.update()
   GameRect = GameLayers.draw(self.screen)
   pygame.display.update(GameRect)

class BattleScene(Scene):
  pass
