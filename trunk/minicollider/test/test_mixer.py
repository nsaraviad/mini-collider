import minicollider.mixer as mixer

sample_rate = 48
beat = sample_rate / 12

mixer.init(sample_rate, beat)

generator = mixer.SoundGenerator()

#~ sound1 = generator.array([0, 0.1, 0.2])
#~ sound2 = generator.array([0.2, 0.4, 0.5])
#~ 
#~ sound3 = sound1 // sound2
#~ sound3.post()
#~ 
#~ sound4 = generator.sine(20, 1)
#~ sound4.plot()

sound5 = generator.array([0.4])
sound5.fill(1).post()
# print generator.noise(0.1).loop(24).play()

base = generator.array([-1, 1])
sound = generator.array([]);
for i in xrange(10,20):
	sound //= base.loop(i).expand().loop(3);
for i in xrange(20,10, -1):
	sound //= base.loop(i).expand().loop(3);
sound.play(1)
exit(0)









