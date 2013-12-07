# -----------------------------------------------------------------------------
# parser.py
#
# Parser para el mini-collider
# -----------------------------------------------------------------------------
import ply.yacc as yacc
from lexer import tokens
import mixer

generator = None

def init(sample_rate, beat, init_pygame=1):
	global generator
	
	mixer.init(sample_rate, beat, init_pygame)
	generator = mixer.SoundGenerator()	

def parse(input):
	return parser.parse(input)

# Parsing rules
precedence = (
	('left','CON','MIX'),
	('left','ADD','SUB'),
	('left','MUL','DIV'),
)

def p_statement_expr(t):
	'START : BUFFER'
	pass

def p_BUFFER_binop(t):
	'''BUFFER :		BUFFER CON BUFFER
				| 	BUFFER MIX BUFFER
				| 	BUFFER ADD BUFFER
				| 	BUFFER SUB BUFFER
				| 	BUFFER MUL BUFFER
				| 	BUFFER DIV BUFFER'''

	if   t[2] in ['con',';'] : t[0] = t[1] // t[3]
	elif t[2] in ['mix','&'] : t[0] = t[1] & t[3]
	elif t[2] in ['add','+'] : t[0] = t[1] + t[3]
	elif t[2] in ['sub','-'] : t[0] = t[1] - t[3]
	elif t[2] in ['mul','*'] : t[0] = t[1] * t[3]
	elif t[2] in ['div','/'] : t[0] = t[1] / t[3]

def p_BUFFER_metodo(t):
	'''BUFFER :		BUFFER PLAY 
				|	BUFFER POST 
				|	BUFFER LOOP 
				|	BUFFER TUNE 
				|	BUFFER FILL 
				|	BUFFER REDU 
				|	BUFFER PLOT 
				|	BUFFER EXPA '''

	if   t[2] == '.play': t[0] = t[1].play(1)
	elif t[2] == '.post': t[0] = t[1].post()
	elif t[2] == '.loop': t[0] = t[1].loop(1)
	elif t[2] == '.tune': t[0] = t[1].tune(1)
	elif t[2] == '.fill': t[0] = t[1].fill(1)
	elif t[2] == '.plot': t[0] = t[1].plot()
	elif t[2] == '.reduce': t[0] = t[1].reduce(1)
	elif t[2] == '.expand': t[0] = t[1].expand(1)
		
def p_BUFFER_metodo_param(t):
	'''BUFFER :		BUFFER PLAY LPAREN NUM RPAREN
				|	BUFFER LOOP LPAREN NUM RPAREN
				| 	BUFFER TUNE LPAREN NUM RPAREN
				| 	BUFFER FILL LPAREN NUM RPAREN
				| 	BUFFER REDU LPAREN NUM RPAREN
				| 	BUFFER EXPA LPAREN NUM RPAREN '''

	if   t[2] == '.play': t[0] = t[1].play(t[4])
	elif t[2] == '.loop': t[0] = t[1].loop(t[4])
	elif t[2] == '.tune': t[0] = t[1].tune(t[4])
	elif t[2] == '.fill': t[0] = t[1].fill(t[4])
	elif t[2] == '.reduce': t[0] = t[1].reduce(t[4])
	elif t[2] == '.expand': t[0] = t[1].expand(t[4])
		
def p_BUFFER_generador_0param(t):
	'''BUFFER :     SIL 
				|	NOI '''

	if   t[1] in ['silence','sil']: t[0] = generator.silence()
	elif t[1] in ['noise','noi']: t[0]   = generator.noise(1)
		
def p_BUFFER_generator_1param(t):
		'''BUFFER :		SIN LPAREN NUM RPAREN
					| 	NOI LPAREN NUM RPAREN '''

		if   t[1] == 'sin': t[0] = generator.sine(t[3], 1)
		elif t[1] in ['noise','noi']: t[0] = generator.noise(t[3])
		
def p_BUFFER_generator_2param(t):
		'''BUFFER :     SIN LPAREN NUM COMA NUM RPAREN
					| 	LIN LPAREN NUM COMA NUM RPAREN '''

		if   t[1] == 'sin': t[0] = generator.sine(t[3], t[5])
		elif t[1] in ['linear','lin']: t[0] = generator.linear(t[3], t[5])
		
def p_BUFFER_llaves(t):
		'''BUFFER : LLLAVE BUFFER RLLAVE '''

		t[0] = t[2]
		
def p_expression_number(t):
		'BUFFER : NUM'

		t[0] = generator.from_list([t[1]])

def p_error(t):
		print("Syntax error at '%s'" % t.value)

parser = yacc.yacc()
