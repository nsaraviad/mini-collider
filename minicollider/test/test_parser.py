import minicollider.parser as parser
import unittest

class TestGeneratorsCases(unittest.TestCase):

	def setUp(self):
		self.sample_rate = 48
		self.beat = self.sample_rate / 12

		parser.init(self.sample_rate, self.beat, 0)
		

	def test_from_list(self):
		pass


if __name__ == '__main__':
	unittest.main()

