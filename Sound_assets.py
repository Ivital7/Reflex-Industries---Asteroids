import pygame, random

pygame.mixer.init()

EXPLODE_VOLUME = 0.7
DAMAGE_VOLUME = 0.7
LASER_VOLUME = 0.87
SUPER_LASER_VOLUME = 0.2
MUSIC_VOLUME = 0.5

#  -- Game sounds --  #

aster_break1 = pygame.mixer.Sound("SOUNDS\\EXPLOSION1.wav")
aster_break1.set_volume(EXPLODE_VOLUME)
aster_break2 = pygame.mixer.Sound("SOUNDS\\EXPLOSION2.wav")
aster_break2.set_volume(EXPLODE_VOLUME)
aster_break3 = pygame.mixer.Sound("SOUNDS\\EXPLOSION3.wav")
aster_break3.set_volume(EXPLODE_VOLUME)
aster_break4 = pygame.mixer.Sound("SOUNDS\\EXPLOSION4.wav")
aster_break3.set_volume(EXPLODE_VOLUME)
base_damage = pygame.mixer.Sound("SOUNDS\\BASE_DAMAGE.wav")
base_damage.set_volume(DAMAGE_VOLUME * 1.1)
aster_damage = pygame.mixer.Sound("SOUNDS\\ASTEROID_DAMAGE.wav")
aster_damage.set_volume(DAMAGE_VOLUME)

asteroid_breaks = (aster_break1, aster_break2, aster_break3, aster_break4)
laser_fire = pygame.mixer.Sound("SOUNDS\\LASER.wav")
laser_fire.set_volume(LASER_VOLUME)
super_laser_fire = pygame.mixer.Sound("SOUNDS\\SUPER_LASER.wav")
super_laser_fire.set_volume(SUPER_LASER_VOLUME)

pygame.mixer.music.load("SOUNDS\\Sountrack_loop.mp3")
pygame.mixer.music.set_volume(MUSIC_VOLUME)


def play_sound(sounds):
    if type(sounds) == tuple:
        random.choice(sounds).play()
    else:
        sounds.play()


def bg_music_start():
    pygame.mixer.music.play(-1, 0.0)


def bg_music_pause():
    pygame.mixer.music.pause()


def bg_music_unpause():
    pygame.mixer.music.unpause()
