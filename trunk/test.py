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

sound = generator.array([-1, 1])
sound.post()
sound = sound.loop(1003).expand().loop(12).play();








