#!/usr/bin/env python
# encoding: utf-8
"""
game.py

Created by C on 2009-07-11.
"""

import pygame, os
from pygame.locals import * 

""" Global Config """
from globals import *

# Resource loading:
DATA_PY = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.normpath(os.path.join(DATA_PY, '..', 'data/fonts/')) 

""" Creates Text Surfaces """
class Text(object):

  def __init__(self, text, size, font, color=(255,255,255)):
    self.text = text
    self.size = size
    self.font = font
    self.color = color
    
    """ Return the Text Surface """
    self.__draw()

  def __draw(self):
    font_obj = pygame.font.Font(os.path.join(DATA_DIR, self.font + ".ttf"), self.size)
    self.render = font_obj.render(self.text, True, self.color)


