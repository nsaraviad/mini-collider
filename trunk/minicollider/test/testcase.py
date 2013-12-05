import minicollider.mixer as mixer
import unittest
import numpy

class TestCase(unittest.TestCase):

	def assertElementsInRange(self, list, min, max):
		for item in list:
			self.assertTrue(min <= item <= max)

	def setUp(self):
		self.sample_rate = 4800
		self.beat = self.sample_rate / 12

		mixer.init(self.sample_rate, self.beat, 0)
		self.generator = mixer.SoundGenerator()
