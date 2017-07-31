# Frozen Garden

Frozen Garden is a collection of simple recursive descent parsers that allow the user to convert a language into psuedocode and flowcharts

The software is split into two main segments, the front-end, which converts to an intermediate XML-style representation, and the back-end, which converts the intermediate code to pseudocode.

The software is designed this way, as it allows the software to be modified for any new languages which may want to be added in the future.

# Usage:

This system currently is only usable through a command line interface. The following is the command syntax:

	python3 main.py [-ilang input_language] [-olang output_language] [files]...

Optionally, the python3 command can be replaced with ./main.py

The currently available input languages are:
 - Python (requires 4 space indentation) (Coming soon)
 - Java (Coming soon)
 - C (Coming soon)

The currently available output languages are:
 - Pseudocode
 - Flowchart (Coming soon)
