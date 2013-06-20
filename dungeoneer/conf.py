import os
from os import path

_DIR_PART, _ = path.split(__file__)

CONF_PATH = path.abspath(path.join(_DIR_PART, os.pardir, 'configs'))
MEDIA_PATH = path.abspath(path.join(_DIR_PART, os.pardir, 'images'))

PIECE_CONFS = filter(lambda f: f.endswith('.yaml'),
    [path.join(CONF_PATH, cfg) for cfg in os.listdir(CONF_PATH)])
