import math
import numpy
import pylab
import pygame


NUMPY_ENCODING = numpy.int16
MIXER_ENCODING = -16

MAX_AMPLITUDE = 32000
SAMPLE_RATE = 8800
BEAT = SAMPLE_RATE / 12


def init(sample_rate=8800, beat=8800/12, init_pygame=1):
	global SAMPLE_RATE, BEAT
	
	SAMPLE_RATE = sample_rate
	BEAT = beat
	
	if init_pygame:
		pygame.mixer.pre_init(SAMPLE_RATE, MIXER_ENCODING, 1)
		pygame.init()


class Sound():
	def __init__(self, samples):
		if (len(samples)) == 0:
			raise Exception('No se puede crear un buffer vacio')

		self.samples = numpy.array(samples, numpy.float)

	def __eq__(self, other):
		return numpy.array_equal(self.samples, other.samples)

	def __iter__(self):
		return self.samples.__iter__()

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

	def play(self, speed=1):
		if not(0 < speed):
			raise Exception("[PLAY] Se esperaba un numero positivo: %s" % speed)
		if speed != 1:
			target = self.resample(int((1.0 / speed) * len(self)))
		else:
			target = self

		amp_mul = MAX_AMPLITUDE / numpy.amax(target.samples)
		samples = numpy.array(target.get_samples() * amp_mul, NUMPY_ENCODING)
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
		if not(0 < count):
			raise Exception("[LOOP] Se esperaba un numero positivo: %s" % count)
		return self.resize(int(count * len(self.samples)))

	def resize(self, new_len):
		if not(isinstance(new_len, int) and 0 < new_len):
			raise Exception("[RESIZE] Se esperaba un entero positivo: %s" % new_len)
		new_samples = numpy.zeros(new_len)
		for i in xrange(new_len):
			new_samples[i] = self.samples[i % len(self.samples)]
		return Sound(new_samples)

	def resample(self, new_len):
		if not(isinstance(new_len, int) and 0 < new_len):
			raise Exception("[RESAMPLE] Se esperaba un entero positivo: %s" % new_len)
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
		if not(0 < count):
			raise Exception("[FILL] Se esperaba un numero positivo: %s" % count)
		new_len = int(BEAT * count)
		
		if (len(self) > new_len): 
			return self.resize(new_len)
		else:
			new_samples = numpy.zeros(new_len)
			for i in xrange(len(self)):
				new_samples[i] = self.samples[i]
			return Sound(new_samples)

	def reduce(self, count=1):
		if not(0 < count):
			raise Exception("[REDUCE] Se esperaba un numero positivo: %s" % count)
		new_len = int(count * BEAT)
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
			b = other.resize(len(self))

		new_samples = numpy.zeros(len(a))
		for i in xrange(len(a)):
			new_samples[i] = op(a.samples[i], b.samples[i])
		return Sound(new_samples)

	def expand(self, count=1):
		if not(0 < count):
			raise Exception("[EXPAND] Se esperaba un numero positivo: %s" % count)
		new_len = int(count * BEAT)
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

	def from_list(self, samples):
		return Sound(numpy.array(samples))

	def sine(self, cicles, amp):
		if not(0<= amp <=1):
			raise Exception("[SINE] Amplitud incorrecta: %s" % amp)
		if not(0 < cicles and isinstance(cicles, int)):
			raise Exception("[SINE] Valor de ciclos incorrecto: %s" % cicles)
		omega = (cicles * numpy.pi * 2) / BEAT
		xvalues = numpy.arange(BEAT) * omega
		return Sound(amp * numpy.sin(xvalues))

	def silence(self):
		return Sound(numpy.zeros(BEAT))

	def linear(self, start, end):
		if not(-1<= start <=1 and -1<= end <=1):
			raise Exception("[LINEAR]  Rango incorrecto: %s, %s" % (start, end))
		return Sound(numpy.linspace(start, end, BEAT))

	def noise(self, amp):
		if not(0<= amp <=1):
			raise Exception("[NOISE] Amplitud incorrecta: %s" % amp)
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



