import math
import numpy
import pylab
import pygame

NUMPY_ENCODING = numpy.int16
MIXER_ENCODING = -16

AMPLITUDE_MULT = 32000
SAMPLE_RATE = 8800
BEAT = SAMPLE_RATE / 12

def init(sample_rate=8800, beat=8800/12):
	global SAMPLE_RATE, BEAT

	SAMPLE_RATE = sample_rate
	BEAT = beat

	pygame.mixer.pre_init(SAMPLE_RATE, MIXER_ENCODING, 1)
	pygame.mixer.init()

class Sound():
	def __init__(self, samples):
		"samples tiene que ser un array de numpy"
		self.samples = samples.copy()

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
		return self._oper(other, (lambda x, y: (x + y) / 2))
		
	def get_samples(self):
		return self.samples

	def set_samples(self, samples):
		self.samples = samples
		return self

	def play(self, times):
		samples = numpy.array(self.copy().loop(times).get_samples() * AMPLITUDE_MULT, NUMPY_ENCODING)
		channel = pygame.sndarray.make_sound(samples).play()
		while channel.get_busy(): pass
		return self

	def plot(self):
		pylab.plot(numpy.arange(int(len(self.samples))), self.samples)
		pylab.show()
		return self

	def post(self):
		print self
		return self

	def loop(self, count):
		return self.resize(int(count) * len(self.samples))

	def resize(self, new_len):
		new_samples = numpy.zeros(new_len)
		for i in xrange(new_len):
			new_samples[i] = self.samples[i % len(self.samples)]
		return Sound(new_samples)

	def resample(self, new_len):
		new_samples = numpy.zeros(new_len)
		for i in xrange(new_len):
			new_samples[i] = self.samples[int(i * len(self) / new_len)]
		return Sound(new_samples)

	def copy(self):
		return Sound(self.samples)

	def concat(self, other):
		new_samples = numpy.concatenate((self.samples, other.samples))
		return Sound(new_samples)

	def tune(self, pitch):
		return self.resample(int(
				len(self) 
				* ( (2**(1.0/12))**(-pitch) )
		))

	def fill(self, count):
		new_len = BEAT * count
		new_samples = numpy.zeros(new_len)
		for i in xrange(len(self.samples)):
			new_samples[i] = self.samples[i]
		return Sound(new_samples)

	def reduce(self, count=1):
		new_len = int(count) * BEAT
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
		return Sound(new_samples)

	def expand(self, count=1):
		new_len = int(count) * BEAT
		if (len(self) < new_len):
			return self.resample(new_len)
		else:
			return self.copy()

	def __str__(self):
		return str(self.samples)

	def tolist(self):
		return self.samples.tolist()

class SoundGenerator():
	def __init__(self):
		pass

	def get_sample_rate(self):
		return SAMPLE_RATE

	def get_beat(self):
		return BEAT

	def get_beats_per_second(self):
		return SAMPLE_RATE / BEAT

	def array(self, samples):
		return Sound(numpy.array(samples))

	def sine(self, cicles, amp):
		omega = (int(cicles) * numpy.pi * 2) / BEAT
		xvalues = numpy.arange(int(BEAT)) * omega
		return Sound(amp * numpy.sin(xvalues))

	def sine_hz(self, hz, amp):
		#~ hz = hz / (SAMPLE_RATE / BEAT)
		samples_per_second = float(SAMPLE_RATE)
	
		seconds_per_period = 1.0 / hz
		samples_per_period = samples_per_second * seconds_per_period

		samples = numpy.array(range(BEAT), numpy.float)
		samples = numpy.sin((samples * 2.0 * math.pi) / samples_per_period) * amp

		return Sound(numpy.array(samples))

	def silence(self):
		return Sound(numpy.zeros(BEAT))

	def linear(self, start, end):
		return Sound(numpy.linspace(start, end, BEAT))

	def noise(self, amp):
		return Sound(numpy.random.random(BEAT) * amp)

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



