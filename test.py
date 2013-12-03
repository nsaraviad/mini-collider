import minicollider

sample_rate = 8000
beat = sample_rate / 12

minicollider.init(sample_rate, beat)

generator = minicollider.SoundGenerator()

sound1 = generator.array([0, 0.1, 0.2])
sound2 = generator.array([0.2, 0.4, 0.5])

sound3 = sound1 // sound2
sound3.post()

# print generator.noise(0.1).loop(24).play()

base = generator.array([-1, 1])
sound = generator.array([]);
for i in xrange(10,20):
	sound //= base.loop(i).expand().loop(3);
for i in xrange(20,10, -1):
	sound //= base.loop(i).expand().loop(3);
sound.play()









