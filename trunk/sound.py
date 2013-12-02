import math
import numpy
import pylab
import pygame

NUMPY_ENCODING = numpy.int16
AMPLITUDE_MULT = 32000

class SoundBuffer():
	def __init__(self, samples, beat):
		"samples tiene que ser un array de numpy"
		self.samples = samples.copy()
		self.beat = beat

	def __len__(self):	
		return len(self.samples)

	def __add__(self, other):
		return self._oper(other, (lambda x, y: x + y))

	def __mul__(self, other):
		return self._oper(other, (lambda x, y: x * y))

	def __sub__(self, other):
		return self._oper(other, (lambda x, y: x - y))

	def __div__(self, other):
		return self._oper(other, (lambda x, y: x / y))

	def __floordiv__(self, other):
		return self.concat(other)

	def __and__(self, other):
		return self.mix(other)

	def mix(self, other):
		pass

	def get_samples(self):
		return self.samples

	def set_samples(self, samples):
		self.samples = samples
		return self

	def play(self):
		samples = numpy.array(self.samples * AMPLITUDE_MULT, NUMPY_ENCODING)
		channel = pygame.sndarray.make_sound(samples).play()
		while channel.get_busy(): pass
		return self

	def plot(self):
		pylab.plot(numpy.arange(int(len(self.samples))), self.samples)
		pylab.show()
		return self

	def post(self):
		print self

	def loop(self, count):
		return self.resize(count * len(self.samples))

	def resize(self, new_len):
		new_samples = numpy.zeros(new_len)
		for i in xrange(new_len):
			new_samples[i] = self.samples[i % len(self.samples)]
		return SoundBuffer(new_samples, self.beat)

	def resample(self, new_len):
		new_samples = numpy.zeros(new_len)
		for i in xrange(new_len):
			new_samples[i] = self.samples[int(i * len(self) / new_len)]
		return SoundBuffer(new_samples, self.beat)

	def copy(self):
		return SoundBuffer(self.samples, self.beat)

	def concat(self, other):
		new_samples = numpy.concatenate((self.samples, other.samples))
		return SoundBuffer(new_samples, self.beat)

	def tune(self, pitch):
		return self.resample(int(
				len(self) 
				* ( (2**(1.0/12))**(-P) )
		))

	def fill(self, count):
		new_len = self.beat * count
		new_samples = numpy.zeros(new_len)
		for i in xrange(new_len):
			new_samples[i] = self.samples[i]
		return SoundBuffer(new_samples, self.beat)

	def reduce(self, count=1):
		new_len = count * self.beat
		if (len(self) > new_len):
			return self.resample(new_len)
		else:
			return self.copy()

	def _oper(self, other, op):
		if (len(self) < len(other)):
			a = self.resize(len(other))
			b = other
		else:
			a = self
			b = other.resize(len(other))

		new_samples = numpy.zeros(len(self))
		for i in xrange(len(self)):
			new_samples[i] = op(self.samples[i], other.samples[i])
		return SoundBuffer(new_samples, self.beat)

	def expand(self, count=1):
		new_len = count * self.beat
		if (len(self) < new_len):
			return self.resample(new_len)
		else:
			return self.copy()

	def __str__(self):
		return str(self.samples)

class SoundGenerator():
	def __init__(self, sample_rate, beat):
		self.sample_rate = sample_rate
		self.beat = beat

	def get_sample_rate(self):
		return self.sample_rate

	def get_beat(self):
		return self.beat

	def get_beats_per_second(self):
		return self.sample_rate / self.beat

	def array(self, samples):
		return SoundBuffer(numpy.array(samples), self.beat)

	def sine(self, cicles, amp):
		omega = (cicles * numpy.pi * 2) / self.beat
		xvalues = numpy.arange(int(self.beat)) * omega
		return SoundBuffer(amp * numpy.sin(xvalues), self.beat)

	def sine_hz(self, hz, amp):
		samples_per_second = float(self.samplerate)
	
		seconds_per_period = 1.0 / hz
		samples_per_period = samples_per_second * seconds_per_period

		samples = numpy.array(range(self.beat), numpy.float)
		samples = numpy.sin((samples * 2.0 * math.pi) / samples_per_period) * amp

		return SoundBuffer(numpy.array(samples), self.beat)

	def silence(self):
		return SoundBuffer(numpy.zeros(self.beat), self.beat)

	def linear(self, start, end):
		pass

	def noise(self, amp):
		pass

	def note(self, note, amp, octave=1):
		freqencies = {
			'C' : 261.63,
			'D' : 293.66,
			'E' : 329.63,
			'F' : 349.23,
			'G' : 392,
			'A' : 440,
			'B' : 493.88
		}
		return self.sine(freqencies[note] * octave / self.get_beats_per_second(), amp)



