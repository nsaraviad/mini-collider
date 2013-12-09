# -----------------------------------------------------------------------------
# lexer.py
#
# Lexer para el mini-collider
# -----------------------------------------------------------------------------
try:
	import ply.lex as lex
except ImportError:
	import external.lex as lex
import re

tokens = (
	'NUM', 'SIN', 'LIN', 'SIL', 'NOI', 'PLAY', 'POST', 'LOOP',
	'TUNE', 'FILL', 'REDU', 'EXPA', 'CON', 'MIX', 'ADD', 'SUB', 'MUL', 
	'DIV', 'LPAREN', 'RPAREN', 'LLLAVE', 'RLLAVE','PLOT', 'COMA',
)

# Tokens

t_SIN         = r'sin'
t_LIN         = r'linear|lin'
t_SIL         = r'silence|sil'
t_NOI         = r'noise|noi'
t_PLAY        = r'.play'
t_POST        = r'.post'
t_LOOP        = r'.loop'
t_TUNE        = r'.tune'
t_FILL        = r'.fill'
t_REDU        = r'.reduce'
t_EXPA        = r'.expand'
t_PLOT        = r'.plot'
t_CON         = r'con|;'
t_MIX         = r'mix|&'
t_ADD         = r'add|\+'
t_SUB         = r'sub|-'
t_MUL         = r'mul|\*'
t_DIV         = r'div|/'
t_LPAREN      = r'\('
t_RPAREN      = r'\)'
t_LLLAVE      = r'\{'
t_RLLAVE      = r'\}'
t_COMA        = r','
t_ignore_COMM = r'//.*\n'
t_ignore_WS   = r'\s|\t|\n'

def t_NUM(t):
	r'\d+(\.\d+)?'
	if t.value.find('.') == -1: 
		t.value = int(t.value)
	else:
		t.value = float(t.value)
		
	return t	
	
def t_error(t):
	raise SyntaxError("Caracter ilegal: '%s'" % t.value[0])
	
# Build the lexer
lexer = lex.lex()
