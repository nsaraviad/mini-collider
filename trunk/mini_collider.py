import minicollider.parser as parser

while 1:
	try:
			s = input('buff > ')   # Use raw_input on Python 2
	except EOFError:
			break
	if s == 'quit':
			break
	parser.parse(s)
