import minicollider.parser as parser
import unittest

class ParserTestCase(unittest.TestCase):


	def setUp(self):

		self.beat = 8
		self.sample_rate = self.beat * 12

		parser.init(self.sample_rate, self.beat, 0)
		self.generator = parser.generator


	def assertParseFail(self, input):
		self.assertRaises(Exception, lambda : parser.parse(input), 
			'Se esperaba un error para el input: %s' % input)


	def assertParseAllFail(self, input_list):
		for input in input_list:
			self.assertParseFail(input)


	def assertParseEqual(self, sound, input):
		self.assertEqual(sound, parser.parse(input))


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


class TestCustomCases(ParserTestCase):
	def test_loop(self):
		pass

if __name__ == '__main__':
	unittest.main()


