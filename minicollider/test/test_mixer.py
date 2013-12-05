import minicollider.mixer as mixer
import unittest

class TestSoundGeneratorCases(unittest.TestCase):

	def setUp(self):
		self.sample_rate = 48
		self.beat = self.sample_rate / 12

		mixer.init(self.sample_rate, self.beat, 0)
		self.generator = mixer.SoundGenerator()

	def test_from_list(self):
		pass


if __name__ == '__main__':
	unittest.main()

