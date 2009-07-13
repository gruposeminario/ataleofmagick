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
DATA_DIR = path.normpath(path.join(DATA_PY, '..', 'data')) 

class load_sprite:
    """
    Load a moving object from a spritesheet.
    """
    def __init__(self, filename):
        self.sheet = pygame.image.load(path.join(DATA_DIR, 'sprites', filename))
        
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

    def load_tile(self, filename):
      img = path.join(DATA_DIR, 'tile', filename + '.png')
      return pygame.image.load(img).convert_alpha()
    

