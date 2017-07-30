#!/usr/bin/env python3

import sys
from lib.parser import LanguageParser, XMLConverter

def handleOption(option, value):
    global options
    if option == 'h':
        print('''Help text!!!''')
        sys.exit()
    elif option == 'ilang':
        options['input_lang'] = value.upper()
    elif option == 'olang':
        options['output_type'] = value.upper()
    else:
        print('FATAL: Invalid Command Line Options. Exiting...')
        sys.exit()

args = sys.argv[1:]
arg = 0

files = []
options = {}

while arg < len(args):
    if args[arg][0] == '-':
        # Handle a command line option
        option = args[arg][1:]
        arg += 1
        value = args[arg]
        handleOption(option, value)
    else:
        files.append(args[arg])
    arg += 1

if files == []:
    print('No files selected. Exiting...')
    sys.exit()

langParser = LanguageParser(options)
xmlConverter = XMLConverter(options)
for f in files:
    print('Converting File: {}'.format(f))
    langParser.setFile(f)
    langParser.evaluate()
    if options.get('output_type', 'INTERMEDIATE_XML') != 'INTERMEDIATE_XML':
        # If converting language, then push the data into the converter before saving
        xmlConverter.setInput(langParser.getOutput())
        xmlConverter.evaluate()
        langParser.setOutput(xmlConverter.getOutput())
        xmlConverter.cleanUp()
    # Save the output and clean up for the next file
    langParser.saveOutput()
    langParser.cleanUp()
    # Print a helpful message
    print('File {} Converted to {}'.format(f, options.get('output_type', 'INTERMEDIATE_XML').lower()))

print('All Files Converted.')
