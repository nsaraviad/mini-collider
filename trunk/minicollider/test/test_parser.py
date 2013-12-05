while 1:
		try:
				s = input('buff > ')   # Use raw_input on Python 2
		except EOFError:
				break
		if s == 'quit':
				break
		yacc.parse(s)
