from back.pseudo_converter import PseudoConverter
import sys

converters = {'PSEUDO':PseudoConverter}

class UnknownConverter:
    def __init__(self, fileText):
        print('Invalid Output Language')
        sys.exit()
