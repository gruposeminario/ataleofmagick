#!/usr/bin/env python
# encoding: utf-8
"""
util.py

Created by C on 2009-07-11.
"""

from os import path  
import pygame
from pygame.locals import *

# Resource loading:
DATA_PY = path.abspath(path.dirname(__file__))
DATA_DIR = path.normpath(path.join(DATA_PY, '..', 'data/sprites/')) 

class load_sprite:
    """
    Load a moving object from a spritesheet.
    """
    def __init__(self, type, filename):
        print "Loading: ", path.join(DATA_DIR, type, filename)
        self.sheet = pygame.image.load(path.join(DATA_DIR, type, filename))

    def get_width(self):
      return self.sheet.get_width()

    def get_height(self):
      return self.sheet.get_height()
        
    def image(self, rect, colorkey = None, alpha = False):
        rect = Rect(rect)
        if alpha:
            image = pygame.Surface(rect.size).convert_alpha()
        else:
            image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image                           
        
    def images(self, rects, colorkey = None):
        imgs = []
        for rect in rects:
            imgs.append(self.image(rect, colorkey))
        return imgs

    
class load_tiles(load_sprite):
  def __init__(self, filename):
    load_sprite.__init__(self, "tiles", filename)

class load_character(load_sprite):
  def __init__(self, filename):
    load_sprite.__init__(self, "characters", filename)

