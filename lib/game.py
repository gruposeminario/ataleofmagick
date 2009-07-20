#!/usr/bin/env python
# encoding: utf-8
"""
game.py

Created by C on 2009-07-11.
"""

from os import environ
import pygame
from pygame.locals import * 
from scene import WorldScene
from character import Character
from maptool  import Map
"""
Set some globals here
Eventually should migrate to a config file
"""
FRAME_SPEED = 30
COLOR_DEPTH = 32
SCREEN_SIZE = (800,600)
GAME_NAME   = "A Tale of Magick"

class Game(object):
  """Controls Gameplay and main loop"""
  def __init__(self):
    self.__initGame()
    self.clock = pygame.time.Clock()
    while self.running:
      self.clock.tick(FRAME_SPEED)
      self.__checkEvents()
      self.__renderScreen()
    self.__exitGame()

  def __initGame(self):
    """ Probably going to be a good idea to move the majority of these configs to a config file 
    ...soon as I create a ini object """
    environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    self.running = True
    self.fullscreen = False
    self.screen = pygame.display.set_mode(SCREEN_SIZE, self.fullscreen, COLOR_DEPTH)
    pygame.display.set_caption(GAME_NAME)
    pygame.mouse.set_visible(False)

    collisionlist = []

    """ Set the Starting Scene """
    self.mainCharacter = Character("Hero")

    """ Create the World """
    self.World = WorldScene(self.screen)
    self.World.addCharacter(self.mainCharacter)
    self.World.setMap(SCREEN_SIZE, (16, 16), "C")

  def __checkEvents(self):
    for event in pygame.event.get():
      if event.type == QUIT:
        self.running = False
      elif event.type == KEYDOWN:
        
        if event.key == K_ESCAPE:
          self.running = False
          
        elif event.key == K_f:
          pygame.display.toggle_fullscreen()

        elif event.key == K_a:
          self.World.addCharacter(self.mainCharacter)
        elif event.key == K_c:
          self.World.removeCharacter(self.mainCharacter)
          
        elif event.key in(K_DOWN, K_UP, K_LEFT, K_RIGHT):
          self.mainCharacter.move_keys.append(pygame.key.name(event.key))
          self.mainCharacter.direction = (self.mainCharacter.move_keys[-1])
          self.mainCharacter.stop = False
          
      elif event.type == KEYUP:
        if event.key in(K_DOWN, K_UP, K_LEFT, K_RIGHT):
          key_id = self.mainCharacter.move_keys.index(pygame.key.name(event.key))
          del self.mainCharacter.move_keys[key_id]
          if len(self.mainCharacter.move_keys) != 0:
            self.mainCharacter.direction = (self.mainCharacter.move_keys[-1])
          else: 
            self.mainCharacter.stop = True
        
    pass
    
  def __renderScreen(self):
    """ Update the Current Game World """
    self.World.update()
    
  def __exitGame(self):
    """docstring for __exitGame"""
    pygame.quit()
    pass
    
 
