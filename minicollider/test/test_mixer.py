import minicollider.mixer as mixer
from minicollider.test.testcase import TestCase
import numpy
import unittest

class TestSoundGeneratorCases(TestCase):


	def test_from_list(self):

		sound = self.generator.from_list([1])
		self.assertEqual([1], sound.tolist())

		sound = self.generator.from_list([0.5])
		self.assertEqual([0.5], sound.tolist())

		sound = self.generator.from_list([0, 0.1, -1])
		self.assertEqual([0, 0.1, -1], sound.tolist())

		self.assertRaises(Exception, lambda : self.generator.from_list([]))
		self.assertRaises(Exception, lambda : self.generator.from_list([2]))
		self.assertRaises(Exception, lambda : self.generator.from_list([-2]))


	def test_silence(self):
		sound = self.generator.silence()
		self.assertEqual([0] * self.beat, sound.tolist())


	def test_linear(self):
		sound = self.generator.linear(0, 0)
		self.assertEqual([0] * self.beat, sound.tolist())

		sound = self.generator.linear(1, 1)
		self.assertEqual([1] * self.beat, sound.tolist())

		sound = self.generator.linear(0.5, 0.5)
		self.assertEqual([0.5] * self.beat, sound.tolist())

		sound = self.generator.linear(-1, -1)
		self.assertEqual([-1] * self.beat, sound.tolist())

		sound = self.generator.linear(0, -1);
		self.assertTrue(numpy.array_equal(numpy.linspace(0, -1, self.beat), sound.get_samples()))		
		self.assertEqual(self.beat, len(sound))

		sound = self.generator.linear(1, -1);
		self.assertTrue(numpy.array_equal(numpy.linspace(1, -1, self.beat), sound.get_samples()))		
		self.assertEqual(self.beat, len(sound))

		sound = self.generator.linear(0, 1);
		self.assertTrue(numpy.array_equal(numpy.linspace(0, 1, self.beat), sound.get_samples()))		
		self.assertEqual(self.beat, len(sound))

		sound = self.generator.linear(-1, 1);
		self.assertTrue(numpy.array_equal(numpy.linspace(-1, 1, self.beat), sound.get_samples()))
		self.assertEqual(self.beat, len(sound))

		self.assertRaises(Exception, lambda : self.generator.linear(2, 0))
		self.assertRaises(Exception, lambda : self.generator.linear(0, 2))


	def test_noise(self):
		sound = self.generator.noise(0)
		self.assertEqual([0] * self.beat, sound.tolist())

		sound = self.generator.noise(1)
		self.assertElementsInRange(sound, -1, 1)
		self.assertEqual(len(numpy.unique(sound.get_samples())), len(sound))
		self.assertEqual(self.beat, len(sound))

		sound = self.generator.noise(0.5)
		self.assertElementsInRange(sound, -0.5, 0.5)
		self.assertEqual(len(numpy.unique(sound.get_samples())), len(sound))
		self.assertEqual(self.beat, len(sound))

		sound = self.generator.noise(0.1)
		self.assertElementsInRange(sound, -0.1, 0.1)
		self.assertEqual(len(numpy.unique(sound.get_samples())), len(sound))
		self.assertEqual(self.beat, len(sound))


	def test_sine(self):
		sound = self.generator.sine(1, 0)
		self.assertEqual([0] * self.beat, sound.tolist())

		sound = self.generator.sine(1, 1)
		self.assertEqual(self.beat, len(sound))
		self.assertElementsInRange(sound, -1, 1)

		sound = self.generator.sine(4, 0.5)
		self.assertEqual(self.beat, len(sound))
		self.assertElementsInRange(sound, -0.5, 0.5)

		self.assertRaises(Exception, lambda : self.generator.sine(0, 1))
		self.assertRaises(Exception, lambda : self.generator.sine(-1, 1))
		self.assertRaises(Exception, lambda : self.generator.sine(0.5, 1))
		self.assertRaises(Exception, lambda : self.generator.sine(1, -1))
		self.assertRaises(Exception, lambda : self.generator.sine(0, 2))


class TestSoundCases(TestCase):


	def test_add(self):

		sound1 = self.generator.from_list([0, 1, -0.5])
		sound2 = self.generator.from_list([0.5, -0.2, 0.5])
		sound3 = sound1 + sound2
		self.assertEqual([0.5, 0.8, 0], sound3.tolist())

		sound1 = self.generator.from_list([0.1])
		sound2 = self.generator.from_list([0, 0.4, 0.5])
		sound3 = sound1 + sound2
		self.assertEqual([0.1, 0.5, 0.6], sound3.tolist())		
		sound4 = sound2 + sound1
		self.assertEqual(sound3, sound4)

		sound1 = self.generator.from_list([0.1, -0.1])
		sound2 = self.generator.from_list([0, 0.5, 0.5, 0.6])
		sound3 = sound1 + sound2
		self.assertEqual([0.1, 0.4, 0.6, 0.5], sound3.tolist())		
		sound4 = sound2 + sound1
		self.assertEqual(sound3, sound4)


	def test_sub(self):

		sound1 = self.generator.from_list([0, 0, -0.5])
		sound2 = self.generator.from_list([0.5, -0.2, 0.5])
		sound3 = sound1 - sound2
		self.assertEqual([-0.5, 0.2, -1], sound3.tolist())

		sound1 = self.generator.from_list([0.1])
		sound2 = self.generator.from_list([0, 0.2, 0.5])
		sound3 = sound1 - sound2
		self.assertEqual([0.1, -0.1, -0.4], sound3.tolist())		

		sound1 = self.generator.from_list([0.1])
		sound2 = self.generator.from_list([0, 0.2, 0.5])
		sound3 = sound2 - sound1
		self.assertEqual([-0.1, 0.1, 0.4], sound3.tolist())		
		
		sound1 = self.generator.from_list([0.1, -0.1])
		sound2 = self.generator.from_list([0, 0.5, 0.5, 0.6])
		sound3 = sound1 - sound2
		self.assertEqual([0.1, -0.6, -0.4, -0.7], sound3.tolist())

		sound1 = self.generator.from_list([0.1, -0.1])
		sound2 = self.generator.from_list([0, 0.5, 0.5, 0.6])
		sound3 = sound2 - sound1
		self.assertEqual([-0.1, 0.6, 0.4, 0.7], sound3.tolist())		


	def test_mul(self):

		sound1 = self.generator.from_list([1, -1, 0.5])
		sound2 = self.generator.from_list([0.5, 0.2, 0.5])
		sound3 = sound1 * sound2
		self.assertEqual([0.5, -0.2, 0.25], sound3.tolist())

		sound1 = self.generator.from_list([0.1])
		sound2 = self.generator.from_list([0, 0.5, -1])
		sound3 = sound1 * sound2
		self.assertEqual([0, 0.05, -0.1], sound3.tolist())		
		sound4 = sound2 * sound1
		self.assertEqual(sound3, sound4)

		sound1 = self.generator.from_list([0.1, -0.1])
		sound2 = self.generator.from_list([0, 0.5, 0.5, 1])
		sound3 = sound1 * sound2
		self.assertEqual([0, -0.05, 0.05, -0.1], sound3.tolist())		
		sound4 = sound2 * sound1
		self.assertEqual(sound3, sound4)


	def test_div(self):

		sound1 = self.generator.from_list([0.5, 0.1, 0.8])
		sound2 = self.generator.from_list([0.5, -0.2, 1])
		sound3 = sound1 / sound2
		self.assertEqual([1, -0.5, 0.8], sound3.tolist())

		sound1 = self.generator.from_list([0.1])
		sound2 = self.generator.from_list([0.5, -0.2, 0.25])
		sound3 = sound1 / sound2
		self.assertEqual([0.2, -0.5, 0.4], sound3.tolist())		

		sound1 = self.generator.from_list([0.5])
		sound2 = self.generator.from_list([0, -0.2, 0.5])
		sound3 = sound2 / sound1
		self.assertEqual([0, -0.4, 1], sound3.tolist())		


	def test_mix(self):

		sound1 = self.generator.from_list([0.5, 0.6, 0])
		sound2 = self.generator.from_list([0.5, 0.2, 1])
		sound3 = sound1 & sound2
		self.assertEqual([0.5, 0.4, 0.5], sound3.tolist())

		sound1 = self.generator.from_list([0.2])
		sound2 = self.generator.from_list([0.5, -0.2, 0.6])
		sound3 = sound1 & sound2
		self.assertEqual([0.35, 0, 0.4], sound3.tolist())
		sound4 = sound2 & sound1	
		self.assertEqual(sound3, sound4)


	def test_concat(self):
		sound1 = self.generator.from_list([0.1])
		sound2 = self.generator.from_list([0.2, 0.3])

		self.assertEqual([0.1, 0.2, 0.3], (sound1 // sound2).tolist())	


	def test_loop(self):
		sound1 = self.generator.from_list([1])
		sound2 = self.generator.from_list([1, 1, 1])
		self.assertEqual(sound2, sound1.loop(3))

		sound1 = self.generator.from_list([1, 0.5])
		sound2 = self.generator.from_list([1, 0.5, 1, 0.5, 1, 0.5])
		self.assertEqual(sound2, sound1.loop(3))

		self.assertRaises(Exception, lambda : sound1.loop(0))
		self.assertRaises(Exception, lambda : sound1.loop(-1))
		self.assertRaises(Exception, lambda : sound1.loop(0.5))
		self.assertRaises(Exception, lambda : sound1.loop(1.5))


	def test_resize(self):
		sound1 = self.generator.from_list([0, 0.1, 0.2])

		self.assertEqual(self.generator.from_list([0]), sound1.resize(1))
		self.assertEqual(self.generator.from_list([0, 0.1]), sound1.resize(2))
		self.assertEqual(self.generator.from_list([0, 0.1, 0.2]), sound1.resize(3))

		self.assertEqual(
			self.generator.from_list([0, 0.1, 0.2, 0.0]), 
			sound1.resize(4))

		self.assertEqual(
			self.generator.from_list([0, 0.1, 0.2, 0.0, 0.1]), 
			sound1.resize(5))

		self.assertEqual(
			self.generator.from_list([0, 0.1, 0.2, 0.0, 0.1, 0.2]), 
			sound1.resize(6))

		self.assertRaises(Exception, lambda : sound1.resize(0))
		self.assertRaises(Exception, lambda : sound1.resize(-1))
		self.assertRaises(Exception, lambda : sound1.resize(0.5))
		self.assertRaises(Exception, lambda : sound1.resize(1.5))


	def test_resample(self):
		sound1 = self.generator.from_list([0, 0.1, 0.2])

		self.assertRaises(Exception, lambda : sound1.resample(0))
		self.assertRaises(Exception, lambda : sound1.resample(-1))
		self.assertRaises(Exception, lambda : sound1.resample(0.5))
		self.assertRaises(Exception, lambda : sound1.resample(1.5))


	def test_copy(self):
		sound1 = self.generator.from_list([0, 0.1, 0.2])
		copy = sound1.copy()

		self.assertEqual(sound1, copy)
		self.assertFalse(sound1 is copy)


	def test_concat(self):
		sound1 = self.generator.from_list([0.1])
		sound2 = self.generator.from_list([0.2])

		self.assertEqual(self.generator.from_list([0.1, 0.2]), sound1.concat(sound2))


	def test_fill(self):
		sound1 = self.generator.from_list([0, 0.1, 0.2])

		self.assertEqual(
			self.generator.from_list([0, 0.1, 0.2] + [0] * (self.beat - 3)),
			sound1.fill(1))
		self.assertEqual(
			self.generator.from_list([0, 0.1, 0.2] + [0] * (self.beat * 2- 3)),
			sound1.fill(2))

		sound2 = self.generator.from_list([0.1] * self.beat)
		self.assertEqual(
			sound2,
			sound2.fill(1))

		self.assertRaises(Exception, lambda : sound1.fill(0))
		self.assertRaises(Exception, lambda : sound1.fill(-1))
		self.assertRaises(Exception, lambda : sound1.fill(0.5))
		self.assertRaises(Exception, lambda : sound1.fill(1.5))


	def test_reduce(self):
		sound1 = self.generator.from_list([0, 0.1] * (self.beat - 1))
		self.assertEqual(self.beat, len(sound1.reduce(1)))

		sound1 = self.generator.from_list([0.1] * (self.beat - 1))
		self.assertEqual(len(sound1), len(sound1.reduce(1)))

		sound1 = self.generator.from_list([0, 0.1] * (self.beat - 1))
		self.assertEqual(len(sound1), len(sound1.reduce(2)))

		self.assertRaises(Exception, lambda : sound1.reduce(0))
		self.assertRaises(Exception, lambda : sound1.reduce(-1))
		self.assertRaises(Exception, lambda : sound1.reduce(0.5))
		self.assertRaises(Exception, lambda : sound1.reduce(1.5))


	def test_expand(self):
		sound1 = self.generator.from_list([0, 0.1, 0.2])
		self.assertEqual(self.beat, len(sound1.expand(1)))
		self.assertEqual(self.beat * 2, len(sound1.expand(2)))

		sound1 = self.generator.from_list([0, 0.1] * self.beat)
		self.assertEqual(len(sound1), len(sound1.expand(1)))

		self.assertRaises(Exception, lambda : sound1.expand(0))
		self.assertRaises(Exception, lambda : sound1.expand(-1))
		self.assertRaises(Exception, lambda : sound1.expand(0.5))
		self.assertRaises(Exception, lambda : sound1.expand(1.5))


	def test_tolist(self):
		sound1 = self.generator.from_list([0, 0.1, 0.2])
		self.assertEqual([0, 0.1, 0.2], sound1.tolist())


	def test_resample(self):
		sound1 = self.generator.from_list([0, 0.1, 0.2, 0.3])

		self.assertEqual(
			self.generator.from_list([0, 0.1, 0.2, 0.3]),
			sound1.resample(4))

		self.assertEqual(1, len(sound1.resample(1)))
		self.assertEqual(3, len(sound1.resample(3)))
		self.assertEqual(6, len(sound1.resample(6)))
		self.assertEqual(10, len(sound1.resample(10)))

		self.assertRaises(Exception, lambda : sound1.expand(0))
		self.assertRaises(Exception, lambda : sound1.expand(-1))
		self.assertRaises(Exception, lambda : sound1.expand(0.5))
		self.assertRaises(Exception, lambda : sound1.expand(1.5))
		


if __name__ == '__main__':
	unittest.main()