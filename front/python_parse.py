import re

class PythonParser:
    def __init__(self, fileText):
        self.text = fileText

    def evaluate(self):
        '''
        Parse the Python into the intermediate XML
        '''
        lines = self.text.split('\n')
        # print(lines)
        node = PythonNode(lines)
        # node.fixCode(lines)
        node.evaluate()

        xmlText = node.treeToXML()
        return '\n'.join(['<program>']+xmlText+['</program>'])

class PythonNode:
    def __init__(self, lines, indentLevel=0):
        self.lines = lines
        self.children = []
        self.indentLevel = indentLevel

    def evaluate(self):
        '''
        Generate the node tree of the Python code
        '''
        l = 0
        # print(self.lines)
        while l < len(self.lines):
            line = self.lines[l]
            # print(line)
            if not line:
                self.children.append(BlankNode())
                l += 1
                continue
            lineTabLevel = (len(line)-len(line.lstrip()))
            if l+1 != len(self.lines) and lineTabLevel < (len(self.lines[l+1])-len(self.lines[l+1].lstrip())):
                innerLines = []
                # print('getting inner lines')
                for a in range(l+1, len(self.lines)):
                    if self.lines[a] != '' and (len(self.lines[a])-len(self.lines[a].lstrip())) <= lineTabLevel:
                        break
                    innerLines.append(self.lines[a])
                self.children.append(self.getNestedNode(l, innerLines, lineTabLevel))
                l = a
                continue
            else:
                # Handle a line of Python
                if len(line.split('=')) == 2:
                    # It's an assignment
                    self.children.append(AssignmentNode(line))
                else:
                    # it's a subcall
                    self.children.append(SubcallNode(line))
                    pass
            l += 1

    def getNestedNode(self, parentLineIndex, innerLines, lineIndent):
        '''
        Get a node that correlates to the nested code type
        '''
        line = self.lines[parentLineIndex].strip()
        if line.startswith('if'):
            return IfNode(line, innerLines, lineIndent)
        elif line.startswith('elif'):
            return ElifNode(line, innerLines, lineIndent)
        elif line.startswith('else'):
            return ElseNode(line, innerLines, lineIndent)
        elif line.startswith('for'):
            return ForNode(line, innerLines, lineIndent)
        elif line.startswith('while'):
            return WhileNode(line, innerLines, lineIndent)
        elif line.startswith('def'):
            return FunctionNode(line, innerLines, lineIndent)
        elif line.startswith('class'):
            return ClassNode(line, innerLines, lineIndent)

    def treeToXML(self):
        '''
        Convert the internal node tree into XML
        '''
        text = []
        for child in self.children:
            # print(child)
            text.append(child.treeToXML())
        return text

    def fixCode(self, lines):
        '''
        Convert multiline code into a single line and remove comments to simplify parsing
        '''
        newLines = []
        a = 0
        while a < len(lines):
            line = lines[a]
            sanitLine = re.sub(r'[\"\'].*?[\'\"]', "''", lines[a])
            if ';' in sanitLine:
                line = line.split(';')
                newLines += line
                continue
            if line.strip().startswith('#'):
                continue
            i = 0
            while line.count("'''")%2 != 0 or sanitLine.count('(') != sanitLine.count(')') or sanitLine.count('{') != sanitLine.count('}'):
                line += lines[a+i]
                i += 1
            newLines.append(line)
            a += i
        return newLines

class SubcallNode:
    def __init__(self, line):
        line = line.strip()
        if line.startswith('return'):
            self.args = ' '+line.split()[1]
            self.target = 'RETURN'
        else:
            self.args = re.findall('\(.*\)', line)
            if len(self.args) >= 1:
                self.args = self.args[0]
            else:
                self.args = '\t'
            self.target = line.strip().split('(')[0]

    def treeToXML(self):
        return '<subcall target="{}" args="{}"/>'.format(self.target, self.args)

class AssignmentNode:
    def __init__(self, line):
        line = line.strip()
        self.var = line.split('=')[0]
        if len(re.findall('[*+/-]=', line)) == 1:
            # it's an operation
            oper = self.var[-1]
            self.var = self.var[:-1]
            self.value = self.var+oper+line.split('=')[1]
        elif 'if' in line:
            # it has an inline condition
            self.value = line.split('=')[1]
        else:
            # it's a standard assignment
            self.value = line.split('=')[1]
        self.value = self.value.strip()
        self.var = self.var.strip()

    def treeToXML(self):
        return '<assignment var="{}" value="{}"/>'.format(self.var, self.value)

class IfNode:
    def __init__(self, line, innerLines, indentLevel):
        node = PythonNode(innerLines, indentLevel)
        node.evaluate()
        self.children = node.children
        self.condition = line.strip()[3:-1]

    def treeToXML(self):
        inside = ''
        for child in self.children:
            inside += child.treeToXML()
        return '<startif><if condition="{}">{}</if>'.format(self.condition, inside)

class ElifNode(IfNode):
    def treeToXML(self):
        inside = ''
        for child in self.children:
            inside += child.treeToXML()
        return '<elif condition="{}">{}</elif>'.format(self.condition[2:], inside)

class ElseNode:
    def __init__(self, line, innerLines, indentLevel):
        node = PythonNode(innerLines, indentLevel)
        node.evaluate()
        self.children = node.children

    def treeToXML(self):
        inside = ''
        for child in self.children:
            inside += child.treeToXML()
        return '<else>{}</else></startif>'.format(inside)

class ForNode:
    def __init__(self, line, innerLines, indentLevel):
        node = PythonNode(innerLines, indentLevel)
        node.evaluate()
        self.children = node.children
        line = line.strip().split()[1:]
        self.var = line[0]
        if 'range(' in ''.join(line):
            args = re.findall('range\(.*\)', ''.join(line))[0][5:]
            # print(args)
            args = tuple([a.strip() for a in args[1:-1].split(',')])
            if len(args) == 1:
                self.start, self.step = [0, 0]
                self.end = args[0]
            else:
                self.start, self.end, self.step = args
        else:
            self.step = '1'
            self.start = '0'
            self.end = line[-1][:-1]+" Length"

    def treeToXML(self):
        inside = ''
        for child in self.children:
            inside += child.treeToXML()
        return '<for var="{}" start="{}" end="{}" step="{}">{}</for>'.format(self.var,
                                    self.start, self.end, self.step, inside)

class WhileNode(IfNode):
    def treeToXML(self):
        inside = ''
        for child in self.children:
            inside += child.treeToXML()
        return '<while condition="{}">{}</while>'.format(self.condition[3:], inside)

class FunctionNode:
    def __init__(self, line, innerLines, indentLevel):
        node = PythonNode(innerLines, indentLevel)
        node.evaluate()
        self.children = node.children
        self.name = line.strip().split()[1]
        self.name = self.name.split('(')[0]

    def treeToXML(self):
        inside = ''
        for child in self.children:
            inside += child.treeToXML()
        return '<routine name="{}">{}</routine>'.format(self.name, inside)

class ClassNode:
    def __init__(self, line, innerLines, indentLevel):
        node = PythonNode(innerLines, indentLevel)
        node.evaluate()
        self.children = node.children

    def treeToXML(self):
        inside = ''
        for child in self.children:
            inside += child.treeToXML()
        return inside

class BlankNode:
    def treeToXML(self):
        return '<br/>'
