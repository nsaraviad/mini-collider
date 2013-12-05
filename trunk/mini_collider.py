import minicollider.parser

minicollider.parser.init(8000, 8000 / 12)

s = '''
sin(21).loop(12).post
'''

minicollider.parser.parse(s)