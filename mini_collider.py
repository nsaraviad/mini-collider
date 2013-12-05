import minicollider.parser

minicollider.parser.init(8000, 8000 / 12)

s = '''
sin(3).plot
'''

minicollider.parser.parse(s)