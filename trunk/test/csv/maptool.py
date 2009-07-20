
import csv, os
import pygame
from pygame.locals import *

SCREEN_WIDTH = 800

class Map(object):

  dimensions = ()
  tiledimensions = ()
  mapname = ""

  tileMap = []

  def __init__(self, dimensions, tiledimensions, mapname, screen):
    self.dimensions = dimensions
    self.tiledimensions = tiledimensions
    self.mapname = mapname
    self.screen = screen

    """ 
      Determine how many tiles should be to a row
      ( SCREENWIDTH / TileWidth )
    """
    self.__tiles_per_row = SCREEN_WIDTH / self.tiledimensions[0]

    """ Attempt to parse the map data """
    self.__read()

  """
    Read in the data from a map file (CSV)
    Parse the data out and move to a dict
  """
  def __read(self):
    mapfile = os.path.join(self.mapname + ".csv")
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
      
  def draw(self):
    """docstring for draw"""
    for row in Map.tileMap:
      print row
    pass

  def update(self):
    """docstring for update"""
    pass

class load_sprite:
    """
    Load a moving object from a spritesheet.
    """
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename)
        
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

"""
MAIN BODY
"""
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.time.Clock().tick(30)
spritesheet = load_sprite("Test.BMP")

Map = Map((100, 100), (16, 16), "Test", screen)

while 1:
  y = 0
  for line in Map.tileMap:
    """ Each new line """
    x = 0
    for tile in line:
     """ Each tile """
     image = spritesheet.image([(int(tile)*16), 0, 16, 16])
     screen.blit(image, (x,y))
     x = (x + 16)
    y = ( y + 16 )
  pygame.display.update()


