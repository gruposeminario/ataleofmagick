
import csv, os
import pygame
from pygame.locals import *
from util import load_tiles
from math import ceil

# Resource loading:
DATA_PY = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.normpath(os.path.join(DATA_PY, '..', 'data/maps/')) 

class Map(object):

  """
    dimensions      = screen x,y
    tiledimensions  = tilesheet invidual tile x,y
    tileMap         = holder for csv data
  """
  dimensions = ()
  tiledimensions = ()
  mapname = ""

  tileMap = []

  def __init__(self, dimensions, tiledimensions, mapname):
    self.dimensions = dimensions
    self.tiledimensions = tiledimensions
    self.mapname = mapname

    """ 
      Determine how many tiles should be to a row
      ( SCREENWIDTH / TileWidth )
    """
    self.__tiles_per_row = dimensions[0] / self.tiledimensions[0]

    """ Attempt to parse the map data """
    self.__read()

  """
    Read in the data from a map file (CSV)
    Parse the data out and move to a dict
  """
  def __read(self):
    mapfile = os.path.join(DATA_DIR + "/" + self.mapname + ".MAP")
    reader = csv.reader(open(mapfile, "rb"), skipinitialspace=True)
    """ 
      At this point we need to take the map data and transform it
      into a list that will determine which terrain tiles to place based
      on the index
    """
    data = []
    end = 0
    for row in reader:
      row = [ elem for elem in row if elem ]
      """ If the length would exceed our tile width """
      if len(data) + len(row) >= self.__tiles_per_row:
        end = self.__tiles_per_row - len(data)
        data.extend(row[0:end])
        self.tileMap.append(data)
        data = []
      else:
        data.extend(row)
      
  def __draw(self):
    """docstring for draw"""
    layer = MapLayer(self.dimensions)
    tilesheet = load_tiles(self.mapname + ".BMP")
    tilesheetdimensions = ( tilesheet.get_width(), tilesheet.get_height() )
    y = 0
    for line in Map.tileMap:
      """ Each new line """
      x = 0
      for tile in line:
       """ Each tile """
       tiles_per_row = ( tilesheetdimensions[0] / self.tiledimensions[0] )
       tiley = ceil( float(tile) / float(tiles_per_row) ) - 1
       image = tilesheet.image([(int(tile)*self.tiledimensions[0]), tiley, self.tiledimensions[0], self.tiledimensions[1]])
       layer.image.blit(image, (x,y))
       x += self.tiledimensions[0]
      y += self.tiledimensions[1]
    return layer

  """ Get most current Map Layer """
  def update(self):
    return self.__draw()

""" Creates a pygame.Surface object for each map """
class MapLayer(pygame.sprite.DirtySprite):
    """
    Creates a map layer.
    """
    def __init__(self, dimensions):
        pygame.sprite.DirtySprite.__init__(self)
        self.dimensions = dimensions
        self.image = pygame.Surface(self.dimensions, SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect()

