import csv, os
import pygame
from pygame.locals import *

""" Global Config """
from globals import *

class Camera(object):

  """ Set Map and Initial Camera Position """
  def __init__(self, map, (x, y), movement_speed):
    self.x, self.y = x, y
    self.current_map = map
    self.speed = movement_speed
    self.width = self.current_map.image.get_width()
    self.height = self.current_map.image.get_height()
    self.map_moving = {
      "up"    : False,
      "down"  : False,
      "right" : False,
      "left"  : False
    }

  """ Checks the hero's camera rectangle against the """
  def check_focus(self, hero, speed):
    
    """ Update the Camera Speed to Match the Hero's """
    self.speed = speed

    """ Define the Hero Camera and Rect Top and Bottom """
    hero_camera_rect, hero_rect = hero.getCamera(), hero.rect

    """ Hero Camera Rectangle Positions """
    hero_camera_bottom = hero_camera_rect.midbottom[1]
    hero_camera_top    = hero_camera_rect.midtop[1]
    hero_camera_left   = hero_camera_rect.midleft[0]
    hero_camera_right  = hero_camera_rect.midright[0]
  
    screen_bottom = self.current_map.rect.midbottom[1]
    screen_top    = self.current_map.rect.midtop[1]
    screen_right  = self.current_map.rect.midright[0]

    if hero_camera_right > G["screen_width"] and (screen_right - G["screen_width"]) > 0 and hero.direction == "right":
      self.x -= self.speed
      self.map_moving["right"] = True
      self.__move_map()
    else:
      self.map_moving["right"] = False

    if hero_camera_left < 0 and hero_camera_left > self.x and hero.direction == "left":
      self.x += self.speed
      self.map_moving["left"] = True
      self.__move_map()
    else:
      self.map_moving["left"] = False

    if hero_camera_bottom > G["screen_height"] and (screen_bottom - G["screen_width"]) > 0 and hero.direction == "down":
      self.y -= self.speed
      self.map_moving["down"] = True
      self.__move_map()
    else:
      self.map_moving["down"] = False

    if hero_camera_top < 0 and self.current_map.rect.y < 0 and hero.direction == "up":
      self.y += self.speed
      self.map_moving["up"] = True
      self.__move_map()
    else:
      self.map_moving["up"] = False

  def __move_map(self):
    self.current_map.rect = self.current_map.image.get_rect(left=self.x, top=self.y)

  def getUpdate(self):
    return self.current_map.rect

  def __str__(self):
    pass
