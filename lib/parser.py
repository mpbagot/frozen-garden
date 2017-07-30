from front import parse_collection
from back import convert_collection as converter_collection

class LanguageParser:
    '''
    A class to convert a language to intermediate XML
    '''
    def __init__(self, options):
        self.language = options.get('input_lang', 'PYTHON')
        self.outputType = options.get('output_type', 'INTERMEDIATE_XML')
        self.fileText = ''
        self.outputText = ''

    def setFile(self, filePath):
        '''
        Set the parser file data with filePath
        '''
        f = open(filePath)
        self.fileText = f.read()
        self.fileName = '.'.join(filePath.split('.')[:-1])+'_'+self.outputType.lower()

    def evaluate(self):
        '''
        Evaluate the data and convert it to the final form
        '''
        parsers = parse_collection.parsers
        parser = parsers.get(self.language, parse_collection.UnknownParser)
        parserInstance = parser(self.fileText)
        self.outputText = parserInstance.evaluate()

    def saveOutput(self):
        '''
        Store the final data in a file in the output folder
        '''
        f = open('output/'+self.fileName, 'w')
        f.write(self.outputText)
        f.close()

    def setOutput(self, text):
        '''
        Set the final output data
        '''
        self.outputText = text

    def getOutput(self):
        '''
        Get the parsed output data
        '''
        return self.outputText

    def cleanUp(self):
        '''
        Clean up the results from the evaluation
        '''
        self.fileText = ''
        self.outputText = ''

class XMLConverter:
    '''
    A class to convert objects to the final form from intermediate XML
    '''
    def __init__(self, options):
        self.language = options.get('output_type', 'PSEUDO')
        self.inputText = ''
        self.outputText = ''

    def setInput(self, inputData):
        '''
        Set the input data for the converter
        '''
        self.inputText = inputData

    def evaluate(self):
        '''
        Run the conversion between the XML to the output language
        '''
        converters = converter_collection.converters
        converter = converters.get(self.language, converter_collection.UnknownConverter)
        converterInstance = converter(self.inputText)
        self.outputText = converterInstance.evaluate()

    def getOutput(self):
        '''
        Get the final output data from the converter
        '''
        return self.outputText

    def cleanUp(self):
        '''
        Clean up the results from the conversion
        '''
        self.inputText = self.outputText = ''
