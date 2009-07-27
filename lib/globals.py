
import ConfigParser, os

# Resource loading:
DATA_PY = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.normpath(os.path.join(DATA_PY, '..', 'data/config/')) 

""" Parse Globals File """
global_config = ConfigParser.ConfigParser()
global_config.read(os.path.join(DATA_DIR, "Globals.ini"))


G,D = {},{}

for pair in global_config.items('game'):
  if pair[1].isdigit() == True:
    value = int(pair[1])
  elif pair[1].lower() == "true":
    value = True
  elif pair[1].lower() == "false":
    value = False
  else:
    value = pair[1]
  G[pair[0]] = value

for pair in global_config.items("debug"):
  if pair[1].lower() == "true":
    value = True
  else:
    value = False
  D[pair[0]] = value
