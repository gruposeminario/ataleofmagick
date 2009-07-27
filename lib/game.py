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
from character import Character, Hero
from map import Map
from menu import MainMenu

""" Global Config """
from globals import *

class Game(object):
  """Controls Gameplay and main loop"""
  def __init__(self):
    self.__initGame()
    while self.running:
      self.clock.tick(G["frame_speed"])
      pygame.display.set_caption(G["name"] + " FPS: " + str(self.clock.get_fps()))
      self.__checkEvents()
      self.__renderScreen()
    self.__exitGame()

  def __initGame(self):
    """ Probably going to be a good idea to move the majority of these configs to a config file 
    ...soon as I create a ini object """
    environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    self.clock = pygame.time.Clock()
    self.running = True
    self.fullscreen = False
    if G["fullscreen"] == True:
      self.screen = pygame.display.set_mode((G["screen_width"], G["screen_height"]), pygame.FULLSCREEN, G["color_depth"])
    else:
      self.screen = pygame.display.set_mode((G["screen_width"], G["screen_height"]), 0, G["color_depth"])
    self.fps = self.clock.get_fps()
    pygame.mouse.set_visible(False)

    self.GameMenu = MainMenu(self.screen)
    self.RunWorld = False

  def __checkEvents(self):

    if self.GameMenu.selection == 0:
      for event in pygame.event.get():

        if event.type == QUIT:
          self.running = False

        elif event.type == KEYDOWN:

          if event.key == K_ESCAPE:
            self.running = False
            
          elif event.key == K_a:
            self.World.addCharacter(self.mainCharacter)
          elif event.key == K_c:
            self.World.removeCharacter(self.mainCharacter)
          
          elif event.key == K_LSHIFT:
            self.mainCharacter.movementspeed += 10

          elif event.key in(K_DOWN, K_UP, K_LEFT, K_RIGHT):
            self.mainCharacter.move_keys.append(pygame.key.name(event.key))
            self.mainCharacter.direction = (self.mainCharacter.move_keys[-1])
            self.mainCharacter.stop = False
            
        elif event.type == KEYUP:

          if event.key == K_LSHIFT:
            self.mainCharacter.movementspeed -= 10

          if event.key in(K_DOWN, K_UP, K_LEFT, K_RIGHT):
            key_id = self.mainCharacter.move_keys.index(pygame.key.name(event.key))
            del self.mainCharacter.move_keys[key_id]
            if len(self.mainCharacter.move_keys) != 0:
              self.mainCharacter.direction = (self.mainCharacter.move_keys[-1])
            else: 
              self.mainCharacter.stop = True

  def __renderScreen(self):
    """ Display the Game's Main Menu, until a option is selected """
    if self.GameMenu.active == True:
      self.GameMenu.run()
    
    if self.GameMenu.selection == 0:
      if self.RunWorld == False:
        collisionlist = []

        self.mainCharacter = Hero("Hero", collisionlist)
        self.World = WorldScene(self.screen)
        self.World.addCharacter(self.mainCharacter)
        self.World.setHero(self.mainCharacter)
        self.World.setMap("BIG")
        self.RunWorld = True
      else:
        self.World.update()
    
  def __exitGame(self):
    """docstring for __exitGame"""
    pygame.quit()
    pass
    
 
