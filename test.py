import pygame
from sound import *

sample_rate = 8000
beat = sample_rate / 12

pygame.mixer.pre_init(sample_rate, -16, 1)
pygame.init()

generator = SoundGenerator(sample_rate, beat)
# sound = generator.sine(23, 1)
sound = generator.note('D', 1)
# sound.plot()
sound = sound.loop(3)
# sound.plot()

base = generator.array([-1, 1])
sound = generator.array([]);

for i in xrange(10,20):
	sound //= base.loop(i).expand().loop(3);
for i in xrange(20,10, -1):
	sound //= base.loop(i).expand().loop(3);

sound.play()









