from front.python_parse import PythonParser
import sys

parsers = {'PYTHON':PythonParser}

class UnknownParser:
    def __init__(self, fileText):
        print('Invalid Input Language')
        sys.exit()
