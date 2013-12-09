import minicollider.parser as parser
import unittest

class ParserTestCase(unittest.TestCase):


	def setUp(self):

		self.beat = 8
		self.sample_rate = self.beat * 12

		parser.init(self.sample_rate, self.beat, 0)
		self.generator = parser.generator


	def assertParseEqualList(self, list, input):
		self.assertParseEqual(self.generator.from_list(list), input)


	def assertParseFail(self, input):
		self.assertRaises(Exception, lambda : parser.parse(input), 
			'Se esperaba un error para el input: %s' % input)


	def assertParseAllFail(self, input_list):
		for input in input_list:
			self.assertParseFail(input)


	def assertParseEqual(self, sound, input):
		parsed_sound = parser.parse(input)
		self.assertEqual(sound, parsed_sound, '%s != %s' % (sound, parsed_sound))


	def assertParseAllEqual(self, sound, input_list):
		for input in input_list:
			self.assertParseEqual(sound, input)


	def assertElementsInRange(self, list, min, max):
		for item in list:
			self.assertTrue(min <= item <= max)

	
class TestGeneratorsCases(ParserTestCase):


	def test_manual(self):
		self.assertParseAllEqual(
			self.generator.from_list([0]),
			['0', '{0}', '{ 0}', '{0 }', '{ 0 }']
		)

		self.assertParseAllEqual(
			self.generator.from_list([1]),
			['1', '{1}', '{ 1}', '{1 }', '{ 1 }']
		)

		self.assertParseAllEqual(
			self.generator.from_list([-1]),
			['-1', '{-1}', '{ -1}', '{-1 }', '{ -1 }']
		)

		self.assertParseAllEqual(
			self.generator.from_list([1]),
			['1.0', '{1.0}', '{ 1.0}', '{1.0 }', '{ 1.0 }']
		)

		self.assertParseAllEqual(
			self.generator.from_list([-0.5]),
			['-0.5', '{-0.5}', '{ -0.5}', '{-0.5 }', '{ -0.5 }']
		)

		self.assertParseAllFail(
			['{', '}', '{ }', '}{', 'a', '-a', 'asd1']	
		)
		
		self.assertParseAllFail(
			['2', '2.0', '1.1', '-2', '-2.1', '0.1.0']	
		)

		self.assertParseAllFail(
			['{2}', '{2.0}', '{1.1}', '{-2}', '{-2.1}']	
		)


	def test_silence(self):
		self.assertParseAllEqual(self.generator.silence(),
			['sil', 'sil()', '{sil}', '{sil()}']
		)

		self.assertParseAllEqual(self.generator.silence(),
			['silence', 'silence()', '{silence}', '{silence()}']
		)

		self.assertParseAllFail(['Sil', 'sile()', 'Silence', 'sil ence'])

		self.assertParseAllFail(['sil(1)', 'sil(1,2)'])


	def test_sine(self):
		self.assertParseEqual(self.generator.sine(1, 1), 'sin(1)')
		self.assertParseEqual(self.generator.sine(5, 1), 'sin(5)')
		self.assertParseEqual(self.generator.sine(11, 1), 'sin(11)')

		self.assertParseEqual(self.generator.sine(1, 0.5), 'sin(1, 0.5)')
		self.assertParseEqual(self.generator.sine(1, 0), 'sin(1, 0)')
		self.assertParseEqual(self.generator.sine(10, 0.2), 'sin(10, 0.2)')

		self.assertParseAllFail(['sin', 'sin()', 'sin(0)','sin(1.0)', 'sin(-1)'])
		self.assertParseAllFail(['sin(1, 0)', 'sin(1, 2)', 'sin(1, -1)'])


	def test_linear(self):
		self.assertParseAllEqual(self.generator.linear(0, 1),
			['linear(0, 1)', 'lin(0, 1)'])

		self.assertParseAllEqual(self.generator.linear(0.5, 0.5),
			['linear(0.5, 0.5)', 'lin(0.5, 0.5)'])

		self.assertParseAllEqual(self.generator.linear(-0.5, 0.5),
			['linear(-0.5, 0.5)', 'lin(-0.5, 0.5)'])

		self.assertParseAllEqual(self.generator.linear(0.5, -0.5),
			['linear(0.5, -0.5)', 'lin(0.5, -0.5)'])

		self.assertParseAllEqual(self.generator.linear(-0.5, -0.5),
			['linear(-0.5, -0.5)', 'lin(-0.5, -0.5)'])

		self.assertParseAllFail(
			['linear', 'linear()', 'lin', 'lin()', 'lin(0)', 'lin(0, 0, 0)'])

		self.assertParseAllFail(
			['lin(2, 0)', 'lin(0, 2)', 'lin(-2, 0)', 'lin(0, -2)',])


	def test_noise(self):
		sound = parser.parse('noi')
		self.assertEqual(self.beat, len(sound))

		sound = parser.parse('noi()')
		self.assertEqual(self.beat, len(sound))

		sound = parser.parse('noise')
		self.assertEqual(self.beat, len(sound))

		sound = parser.parse('noise()')
		self.assertEqual(self.beat, len(sound))

		sound = parser.parse('noi(0)')
		self.assertEqual(self.generator.silence(), sound)
		
		sound = parser.parse('noi(0.5)')
		self.assertEqual(self.beat, len(sound))
		self.assertElementsInRange(sound, -0.5, 0.5)

		self.assertParseAllFail(['noi(2)', 'noi(-2)'])


class TestOperatorCases(ParserTestCase):


	def test_add(self):

		self.assertParseEqualList([3], '1 + 2')
		self.assertParseEqualList([6], '1 + 2 + 3')
		self.assertParseEqualList([-1], '1 + 2 + -4')
		self.assertParseEqualList([2, 5, -1], '{1; 2; 3} + {1; 3; -4}')
		self.assertParseEqualList([2, 5, -1], '{1; 4; -2} + {1}')
		self.assertParseEqualList([2, 5, -1], '{1; 4; -2} + 1')
		self.assertParseEqualList([2, 5, -1, 0], '{1; 3; -2; -2} + {1; 2}')
		self.assertParseEqualList([2, 5, -1, 0], '{1; 2} + {1; 3; -2; -2}')


	def test_sub(self):

		self.assertParseEqualList([-1], '1 - 2')
		self.assertParseEqualList([-4], '1 - 2 - 3')
		self.assertParseEqualList([3], '1 - 2 - -4')
		self.assertParseEqualList([0, -1, 7], '{1; 2; 3} - {1; 3; -4}')
		self.assertParseEqualList([0, 3, -3], '{1; 4; -2} - {1}')
		self.assertParseEqualList([0, 3, -3], '{1; 4; -2} - 1')
		self.assertParseEqualList([0, 1, -3, -4], '{1; 3; -2; -2} - {1; 2}')
		self.assertParseEqualList([0, -1, 3, 4], '{1; 2} - {1; 3; -2; -2}')


	def test_mul(self):

		self.assertParseEqualList([2], '1 * 2')
		self.assertParseEqualList([6], '1 * 2 * 3')
		self.assertParseEqualList([-8], '1 * 2 * -4')
		self.assertParseEqualList([1, 6, -12], '{1; 2; 3} * {1; 3; -4}')
		self.assertParseEqualList([2, 8, -4], '{1; 4; -2} * {2}')
		self.assertParseEqualList([2, 8, -4], '{1; 4; -2} * 2')
		self.assertParseEqualList([1, 6, -2, -4], '{1; 3; -2; -2} * {1; 2}')
		self.assertParseEqualList([1, 6, -2, -4], '{1; 2} * {1; 3; -2; -2}')


	def test_div(self):

		self.assertParseEqualList([5], '10 / 2')
		self.assertParseEqualList([2], '12 / 2 / 3')
		self.assertParseEqualList([-2], '16 / 2 / -4')
		self.assertParseEqualList([3, 0.5, -0.25], '{3; 2; 1} / {1; 4; -4}')
		self.assertParseEqualList([5, 2, -0.5], '{10; 4; -1} / {2}')
		self.assertParseEqualList([5, 2, -0.5], '{10; 4; -1} / 2')
		self.assertParseEqualList([1, 1.5, -2, -1], '{1; 3; -2; -2} / {1; 2}')
		self.assertParseEqualList([1, 1, -0.5, -1.5], '{1; 3} / {1; 3; -2; -2}')


	def test_div(self):

		self.assertParseEqualList([5], '10 / 2')
		self.assertParseEqualList([2], '12 / 2 / 3')
		self.assertParseEqualList([-2], '16 / 2 / -4')
		self.assertParseEqualList([3, 0.5, -0.25], '{3; 2; 1} / {1; 4; -4}')
		self.assertParseEqualList([5, 2, -0.5], '{10; 4; -1} / {2}')
		self.assertParseEqualList([5, 2, -0.5], '{10; 4; -1} / 2')
		self.assertParseEqualList([1, 1.5, -2, -1], '{1; 3; -2; -2} / {1; 2}')
		self.assertParseEqualList([1, 1, -0.5, -1.5], '{1; 3} / {1; 3; -2; -2}')


	def test_mix(self):

		self.assertParseEqualList([6], '10 & 2')
		self.assertParseEqualList([5], '12 & 2 & 3')
		self.assertParseEqualList([2.5], '16 & 2 & -4')
		self.assertParseEqualList([2, 3, -1.5], '{3; 2; 1} & {1; 4; -4}')
		self.assertParseEqualList([6, 3, 0.5], '{10; 4; -1} & {2}')
		self.assertParseEqualList([6, 3, 0.5], '{10; 4; -1} & 2')
		self.assertParseEqualList([1, 2.5, -0.5, 0], '{1; 3; -2; -2} & {1; 2}')
		self.assertParseEqualList([1, 2.5, -0.5, 0], '{1; 2} & {1; 3; -2; -2}')


	def test_concat(self):

		self.assertParseEqualList([10, 2], '10 ; 2')
		self.assertParseEqualList([10, 2, -3], '10 ; 2 ; -3')

		self.assertParseEqualList([10, 2], '{10} ; {2}')
		self.assertParseEqualList([10, 1, 2], '{10; 1} ; {2}')
		self.assertParseEqualList([10, 2, 1], '{10} ; {2; 1}')
		self.assertParseEqualList([1, 2, 3, 4, 5, 6], '{1; 2} ; {3; 4} ; {5; 6}')


class TestMethodsCases(ParserTestCase):


	def test_loop(self):

		self.assertParseEqualList([5], '5.loop()')
		self.assertParseEqualList([5], '5.loop')

		self.assertParseEqualList([1, 1], '1.loop(2)')
		self.assertParseEqualList([1, 1], '{1}.loop(2)')

		self.assertParseEqualList([1, 2], '{1 ; 2}.loop(1)')
		self.assertParseEqualList([1, 2] * 2, '{1 ; 2}.loop(2)')
		self.assertParseEqualList([1, 2] * 10, '{1 ; 2}.loop(10)')

		self.assertParseEqualList([1], '{1 ; 2}.loop(0.5)')
		self.assertParseEqualList([1, 2, 1], '{1 ; 2}.loop(1.5)')

		self.assertParseFail('1.loop(0)')
		self.assertParseFail('1.loop(-1)')


	def test_fill(self):

		self.assertParseEqualList([1] + [0] * (self.beat - 1), '1.fill(1)')
		self.assertParseEqualList([1] + [0] * (self.beat - 1), '1.fill()')
		self.assertParseEqualList([1] + [0] * (self.beat - 1), '1.fill')

		self.assertParseEqualList([1, 2, 3] + [0] * (self.beat - 3), '{1;2;3}.fill')
		self.assertParseEqualList([1, 2, 3] + [0] * (self.beat * 2 - 3), '{1;2;3}.fill(2)')

		self.assertParseEqualList([1 ] + [0] * (self.beat / 2 - 1), '1.fill(0.5)')
		self.assertParseEqualList([1, 2] * (self.beat / 2), '{1;2}.loop(1000).fill')

		self.assertParseFail('1.fill(0)')
		self.assertParseFail('1.fill(-1)')


	def test_reduce(self):

		self.assertParseEqualList([1], '1.reduce')
		self.assertParseEqualList([1], '1.reduce()')
		self.assertParseEqualList([1, 2] * (self.beat / 2), '{1; 2}.loop(100).reduce')
		self.assertParseEqualList([2] * self.beat, '2.loop(1000).reduce()')
		self.assertParseEqualList([2] * (self.beat * 2), '2.loop(1000).reduce(2)')

		self.assertParseFail('1.reduce(0)')
		self.assertParseFail('1.reduce(-1)')		


	def test_expand(self):

		self.assertParseEqualList([1] * self.beat, '1.expand')
		self.assertParseEqualList([1] * self.beat, '1.expand()')
		self.assertParseEqualList([1] * (self.beat / 2) + [2] * (self.beat / 2), '{1;2}.expand()')
		self.assertParseEqualList([1] * self.beat + [2] * self.beat , '{1;2}.expand(2)')
		self.assertParseEqualList([1] * 1000, '1.loop(1000).expand()')

		self.assertParseFail('1.expand(0)')
		self.assertParseFail('1.expand(-1)')		


class TestPrecedenceCases(ParserTestCase):		


	def test_add_mul(self):
		self.assertParseEqualList([7], '1 + 2 * 3')
		self.assertParseEqualList([7], '2 * 3 + 1')
		self.assertParseEqualList([8], '2 * {3 + 1}')
		self.assertParseEqualList([8], '{3 + 1} * 2')


	def test_add_div(self):

		self.assertParseEqualList([4], '1 + 9 / 3')
		self.assertParseEqualList([3], '6 / 3 + 1')
		self.assertParseEqualList([2], '8 / {3 + 1}')
		self.assertParseEqualList([2], '{3 + 1} / 2')


	def test_add_sub(self):

		self.assertParseEqualList([0], '1 + 2 - 3')
		self.assertParseEqualList([2], '1 - 2 + 3')
		self.assertParseEqualList([-4], '1 - 2 + -3')
		self.assertParseEqualList([6], '1 + 2 - -3')


	def test_add_concat(self):

		self.assertParseEqualList([6, 3], '1 + 5 ; 3')
		self.assertParseEqualList([6, 3, 1.5], '1 + 5 ; 3 ; 0.5 + 1')


	def test_sub_concat(self):

		self.assertParseEqualList([-4, 3], '1 - 5 ; 3')
		self.assertParseEqualList([-4, 3, -0.5], '1 - 5 ; 3 ; 0.5 - 1')


	def test_mul_concat(self):

		self.assertParseEqualList([10, 3], '2 * 5 ; 3')
		self.assertParseEqualList([10, 3, 1], '2 * 5 ; 3 ; 0.5 * 2')


	def test_div_concat(self):

		self.assertParseEqualList([2, 3], '10 / 5 ; 3')
		self.assertParseEqualList([2, 3, 0.25], '10 / 5 ; 3 ; 0.5 / 2')


	def test_loop_concat(self):

		self.assertParseEqualList([1, 1, 1, 3], '1.loop(3) ; 3')
		self.assertParseEqualList([3, 1, 1, 1], '3 ; 1.loop(3)')


	def test_expand_concat(self):

		self.assertParseEqualList([1] * self.beat + [3], '1.expand ; 3')
		self.assertParseEqualList([3] + [1] * self.beat, '3 ; 1.expand')


	def test_reduce_concat(self):

		self.assertParseEqualList([1, 2, 3], '{1;2}.reduce ; 3')
		self.assertParseEqualList([3, 1, 2], '3 ; {1;2}.reduce')


	def test_fill_concat(self):

		self.assertParseEqualList([1, 2] + [0] * (self.beat - 2) + [3], '{1;2}.fill ; 3')
		self.assertParseEqualList([3] + [1, 2] + [0] * (self.beat - 2), '3 ; {1;2}.fill')


	def test_add_mix(self):

		self.assertParseEqualList([4.5], '1 + 5 & 3')
		self.assertParseEqualList([4], '3 & 4 + 1')

	def test_loop_mix(self):

		self.assertParseEqualList([2, 2, 2], '1.loop(3) & 3')
		self.assertParseEqualList([2, 2, 2], '3 & 1.loop(3)')


class TestCustomCases(ParserTestCase):


	def test_enunciado(self):
		
		self.assertParseEqualList([1, 2], '1; 2')
		self.assertParseEqualList([1, 2], '{1; 2}')
		self.assertParseEqualList([7], '{1 + 2*3}')
		self.assertParseEqualList([6, 3, 6], '{{2;1} mul {3;3;3}}')
		self.assertParseEqualList([0, 1], '{1-1;2-1}')
		self.assertParseEqualList([2, 3, 4], '{4+1*-2 & {2;4;6}}')
		self.assertParseEqualList([0, 1, 1], '{0;1.loop(2)}')
		self.assertParseEqualList([0, 1], '{0;1;2;3}.loop(0.5)')


if __name__ == '__main__':
	unittest.main()



