from glob import glob

import yaml

from dungeoneer import conf

game_pieces = []
game_pieces_by_name = {}

class Piece(object):
    """
    Intensely Flexible container class
    """
    def __init__(self, name, image, **kwargs):        
        
        self.name = name
        self.image = image
        self.__dict__.update(kwargs)

    def __getattr__(self, name):
        return self.__dict__.get(name, None)

    def __setattr__(self, name, value):
        self.__dict__[name] = value
                
    def __getitem__(self, name):
        return self.__dict__.get(name, None)

    def __setitem__(self, name, value):
        self.__dict__[name] = value

    def items(self):
        return self.__dict__.items()
        
def _create_piece(config): 
    new_piece = Piece(**config)
    game_pieces.append(new_piece)
    game_pieces_by_name[new_piece.name] = new_piece
    

for piece_conf in conf.PIECE_CONFS:    
    with open(piece_conf, 'r') as configfile:
        config = yaml.load(configfile)
    _create_piece(config)
