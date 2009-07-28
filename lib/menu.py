#!/usr/bin/env python
# encoding: utf-8
"""
game.py

Created by C on 2009-07-11.
"""

import pygame, os, time
from sys import exit
from pygame.locals import * 
from text import Text
from util import load_image

""" Global Config """
from globals import *

""" Generic Menu Class """
class Menu(object):
  
  def __init__(self, screen):
    self.running = True
    self.display = screen
    self.selection = ""
    self.key_pressed   = ""

  """ Check Menu Events """
  def checkEvents(self):
    
    for event in pygame.event.get():

     if event.type == KEYDOWN:
      keyname = pygame.key.name(event.key)

      if event.key in(K_DOWN, K_UP, K_LEFT, K_RIGHT, K_RETURN):
        self.selection = ""
        if keyname == "down" or keyname == "right":
          self.current_option += 1
        elif keyname == "up" or keyname == "left":
          self.current_option -= 1
        elif keyname == "return":
          self.selection = self.current_option

    """ Adjust the Menu """
    if self.current_option == len(self.MenuOptions):
      self.current_option = 0
    if self.current_option < 0:
      self.current_option = len(self.MenuOptions) - 1

  def update(self):
    self.display.blit(self.background, (0,0)) 
    self.draw()
    pygame.display.update()

  """ Run the Display For The Menu """
  def run(self):
    while self.active == True:
      self.checkEvents()
      self.handleSelection()
      self.update()

  def transition(self, menu):
    self.fade_out()
    menu.run()

  def fade_in(self):
    alpha, timer = 255, 0
    white = pygame.Surface((G["screen_width"], G["screen_height"]))
    white.fill((255,255,255))

    while alpha > 0:
      timer -= 1
      if timer <= 0:
        timer = 10
        alpha -= 35
      white.set_alpha(alpha)
      self.update()
      self.display.blit(white, (0,0))
      pygame.display.update()

  def fade_out(self):
    alpha, timer = 255, 0
    backup = pygame.display.get_surface().copy()
    white = pygame.Surface((G["screen_width"], G["screen_height"]))
    white.fill((255,255,255))

    while alpha > 0:
      timer -= 1
      if timer <= 0:
        timer = 10
        alpha -= 35
      backup.set_alpha(alpha)
      self.display.blit(white, (0,0))
      self.display.blit(backup, (0,0))
      pygame.display.update()


  """ Meant to be Overloaded """
  def draw(self):
    pass

  """ Meant to be Overloaded """
  def handleSelection(self):
    pass

""" A Blank Menu """
class BlankMenu(Menu):

  def __init__(self, screen):
    Menu.__init__(self, screen)
    self.x = 180
    self.y = 125
    self.increment = 40
    self.active = True
    self.current_option = 0
    self.background = load_image("ATOM.png")
    self.MenuOptions = ["Go Back"]

  
  """ Handle Selection """
  def handleSelection(self):
    if isinstance(self.selection, int):

      """ Load Game Menu """
      if self.selection == 0:
        self.active = False

  """ Draw the Menu """
  def draw(self):
    y = self.y

    text = Text("[Not Yet Implemented]", 18, "GameOption", (255, 255, 255))
    self.display.blit(text.render, (self.x, self.y + 220))

    for i, option in enumerate(self.MenuOptions):
      if self.selection == i:
        color = (255, 0, 0)
      elif self.current_option == i:
        color = (255, 255, 0)
      else:
        color = (255, 255, 255)

      text = Text(option, 22, "GameOption", color)
      self.display.blit(text.render, (self.x, y))
      y += self.increment

""" Main Menu """
class MainMenu(Menu):

  def __init__(self, screen):
    Menu.__init__(self, screen)
    self.x = 180
    self.y = 125
    self.increment = 40
    self.active = True
    self.current_option = 0
    self.background = load_image("ATOM.png")
    self.MenuOptions = ["Begin Adventure", "Load Adventure", "Settings", "Quit"]

  """ Handle Selection """
  def handleSelection(self):
    if isinstance(self.selection, int):

      """ Start Game """
      if self.selection == 0:
        self.active = False
      
      """ Load Game """
      if self.selection == 1:
        self.selection = ""
        NoMenu = BlankMenu(self.display)
        self.transition(NoMenu)
  
      """ Settings """
      if self.selection == 2:
        self.selection = ""
        NoMenu = BlankMenu(self.display)
        NoMenu.run()

      """ Quit """
      if self.selection == len(self.MenuOptions) - 1:
        exit()

  """ Draw the Menu """
  def draw(self):
    y = self.y

    text = Text("A Game Developed By: Chris A.W.", 18, "GameOption", (255, 255, 255))
    self.display.blit(text.render, (self.x, self.y + 220))

    for i, option in enumerate(self.MenuOptions):
      if self.selection == i:
        color = (255, 0, 0)
      elif self.current_option == i:
        color = (255, 255, 0)
      else:
        color = (255, 255, 255)

      text = Text(option, 22, "GameOption", color)
      self.display.blit(text.render, (self.x, y))
      y += self.increment

