#!/usr/bin/env python3

from front.xml_parse import XMLParser

class PseudoConverter:
    def __init__(self, fileText):
        self.text = fileText

    def evaluate(self):
        '''
        Return the converted text
        '''
        xmlTree = XMLParser(self.text).tree
        self.text = self.getFromTree(xmlTree)
        return '\n'.join(self.text)

    def getFromTree(self, tree, pad=''):
        '''
        Get the final Pseudocode from the xml tree
        '''
        text = []
        for tag in tree:
            code = self.getPseudoCode(tag)
            if code:
                text.append(pad+code)
            if len(tag.children) != 0:
                # get the child code by recursing
                text += self.getFromTree(tag.children, pad+('\t' if tag.name not in ('startif', 'program') else ''))
            code = self.getPseudoCode(tag, False)
            if code:
                text.append(pad+code)
        return text

    def getPseudoCode(self, tag, isOpening=True):
        '''
        Get the pseudocode of the tag, either opening or closing
        '''
        if isOpening:
            if tag.name == 'routine':
                return 'BEGIN {}'.format(tag.attributes['name'])
            elif tag.name == 'assignment':
                return 'SET {} TO {}'.format(tag.attributes['var'], tag.attributes['value'])
            elif tag.name == 'for' or tag.name == 'iterfor':
                return 'FOR {} = {} TO {} STEP {}'.format(tag.attributes['var'], tag.attributes['start'], tag.attributes['end'], tag.attributes['step'])
            elif tag.name == 'while':
                return 'WHILE {}'.format(tag.attributes['condition'])
            elif tag.name == 'repeat':
                return 'REPEAT'
            elif tag.name == 'switch':
                return 'CASEWHERE {} EVALUATES TO'.format(tag.attributes['expression'])
            elif tag.name == 'case':
                return tag.attributes['value']+':'
            elif tag.name == 'default':
                return 'OTHERWISE:'
            elif tag.name == 'if':
                return 'IF '+tag.attributes['condition']
            elif tag.name == 'elif':
                return 'ELSE IF '+tag.attributes['condition']
            elif tag.name == 'else':
                return 'ELSE'
            elif tag.name == 'subcall':
                return tag.attributes['target']+tag.attributes['args']
        else:
            if tag.name == 'routine':
                return 'END {}'.format(tag.attributes['name'])
            elif tag.name == 'for':
                return 'ENDFOR'
            elif tag.name == 'iterfor':
                return 'NEXT {}'.format(tag.attributes['var'])
            elif tag.name == 'while':
                return 'ENDWHILE'
            elif tag.name == 'repeat':
                return 'UNTIL {}'.format(tag.attributes['condition'])
            elif tag.name == 'switch':
                return 'ENDCASE'
            elif tag.name == 'startif':
                return 'ENDIF'
        return ''
