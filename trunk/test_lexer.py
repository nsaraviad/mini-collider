from lexer import lexer 

# Test it out
data = '''
{ { 1 - 2} con sin(-3) }.play
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: break      # No more input
    print tok


