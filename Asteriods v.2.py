"""
Project Title: 
Asteroids

Description:
A reimagining of the classic arcade game Asteroids

Authors:
Jerry Aska (...from Antigua)
Mathieu Dario
Warren James
Inoela Vital
"""


import pygame
import sys
import random
import time

from pygame.locals import *
from Sound_assets import *

pygame.init()

# colour   R    G    B

WHITE  = (255, 255, 255)
BLACK  = (  0,   0,   0)
RED    = (255,   0,   0)
GREEN  = (  0, 255,   0)
ORANGE = (255, 128,   0)
YELLOW = (255, 255,   0)
BLUE   = (0  ,   0, 255)  

list_bullets=[]
list_asteroids=[]
FPS = 60 # frames per second setting
fpsClock = pygame.time.Clock()

SCREEN_WIDTH = SCREEN_HEIGHT = 700
NUMBER_OF_WAVES = 3
SCORE = 0 # Initialise score as 0
speed_up = False
text_score = 'Score : ' + str(SCORE)
loss_text = "You Lose"
win_text = "You Win"
font_Score = pygame.font.Font('freesansbold.ttf', 20)
font_END = pygame.font.SysFont("Impact", 48)
win_surf = font_END.render(win_text, True, WHITE, BLACK)
loss_surf = font_END.render(loss_text, True, WHITE, BLACK)

score_Surf = font_Score.render(text_score, True, WHITE, BLACK)
textRectObj = score_Surf.get_rect()
textRectObj.topleft = (10, 10)


class Ship:
    "Ship Object"
    def __init__(self, x, y, speed):
        self.pos_x = (x*.5)
        self.pos_y = (y*0.85)
        self.vel = speed

    def update_pos(self, direction):
        if direction == "left":
            self.pos_x-=self.vel
        if direction == "right":
            self.pos_x+=self.vel

    def display(self, x, y):
        pygame.draw.polygon(DISPLAYSURF,WHITE, ((self.pos_x, self.pos_y), (self.pos_x -  x//60, self.pos_y + y//40), (self.pos_x, self.pos_y + y//60), (self.pos_x + x//60,  self.pos_y + y//40)))
 

class Bullet:
    "Bullet Object"

    def __init__(self, pos_x, pos_y, radius=1):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel = SCREEN_HEIGHT / 100
        self.radius = radius
        play_sound(laser_fire)

    def update_pos(self):
        self.pos_y -= self.vel


def gen_bullet(pos_x, pos_y, r=1):
    list_bullets.append(Bullet(pos_x, pos_y, r))


def del_bullet(list_bullets):
    for bullet_i in list_bullets:
        if bullet_i.pos_y<=0:
            list_bullets.remove(bullet_i)


def bullet_disp():
    """ Print on the screen the asteroids """
    for bullet_i in range(len(list_bullets)):
        list_bullets[bullet_i].update_pos()
        x_coor = int(list_bullets[bullet_i].pos_x)
        y_coor = int(list_bullets[bullet_i].pos_y)
        r = list_bullets[bullet_i].radius
        pygame.draw.circle(DISPLAYSURF, WHITE, (x_coor,y_coor), r)


class Asteroid:
    """ Asteroid object """

    def __init__(self, size, vel, position_x, position_y=0.0):
        """ Define attributes """

        self.pos_x = position_x
        self.pos_y = position_y

        self.vect_x = 0.0
        self.vect_y = vel * 2.0

        self.radius_asteroid = 3 + 2*size
        self.width = size

        self.life = size
        
    def update_pos(self, d_time):
        """ Update the position with the vector coordonate """

        self.pos_x += self.vect_x * d_time
        self.pos_y += self.vect_y * d_time
        

def asteroid_gen():
    """ Generate one asteroid """

    nb_of_object = random.randint(0,4)
    list_quarter = [[50, 180], [210, 340], [360, 490], [520, 650]]

    for obj_i in range(nb_of_object):

        # way to avoid any troubles with asteroids to much close#
        size = random.randint(1, 4)
        quarter = random.choice(list_quarter)
        list_quarter.remove(quarter)

        x = random.randint(quarter[0], quarter[1])
        s = (random.random() * 3) + 14.0
        aster = Asteroid(size, s, x)
        
        list_asteroids.append(aster)

    return nb_of_object


def collision(list_bullets, list_asteroids, SCORE):
    #  Loops through all asteroids and bullets between the two list and checks if any bullet lies within the range of an asteroid"""
    hits = 0
    for bullet_i in list_bullets:
        for aster_i in list_asteroids:
            if (bullet_i.pos_x > aster_i.pos_x-aster_i.radius_asteroid * 1.1) and (bullet_i.pos_x < aster_i.pos_x + aster_i.radius_asteroid * 1.1):
                if (bullet_i.pos_y > aster_i.pos_y-aster_i.radius_asteroid * 1.1) and (bullet_i.pos_y < aster_i.pos_y + aster_i.radius_asteroid * 1.1):

                    play_sound(aster_damage)
                    list_bullets.remove(bullet_i)
                    aster_i.life -= 1
                    aster_i.radius_asteroid -= 2
                    aster_i.width - 1
                    hits += 1
                    SCORE = update_score('hit', SCORE)

                if aster_i.life == 0:
                    play_sound(asteroid_breaks)
                    list_asteroids.remove(aster_i)                    
    return hits, SCORE


# BOSS LIFE
def boss_collision(list_bullets, boss_x, boss_y):
    boss_damage = 0
    for bullet_i in list_bullets:
        if (bullet_i.pos_x > boss_x -30) and (bullet_i.pos_x < boss_x +30):
            if (bullet_i.pos_y > boss_y-30)and(bullet_i.pos_y < boss_y+30):
                list_bullets.remove(bullet_i)
                boss_damage += 1
    return boss_damage


def boss_life_tracker(total_boss_life, boss_hit, boss_x, boss_y):
        boss_life_length = total_boss_life -(boss_hit*2)
        if boss_life_length >= 0:
            COLOR = BLACK
            if boss_life_length > 0.75 * total_boss_life:
                COLOR = GREEN
            elif boss_life_length > 0.5 * total_boss_life:
                COLOR = ORANGE
            elif boss_life_length > 0 * total_boss_life:
                COLOR = RED 
            pygame.draw.rect(DISPLAYSURF, COLOR, (boss_x - SCREEN_WIDTH // 35, boss_y + SCREEN_HEIGHT // 30, boss_life_length, SCREEN_HEIGHT // 80)) #draws health bar
        else:
            end_of_game()


#  GROUND COLLISIONS
def ground_collision(list_asteroids, score):
    damage = 0
    for aster_i in list_asteroids:
        if (aster_i.pos_y >= player.pos_y+SCREEN_HEIGHT // 21):
            damage += 1
            list_asteroids.remove(aster_i)
            score = update_score('hurt', score)
            play_sound(base_damage)


            lose_life = True
        else:
            lose_life = False

    return damage, score


def asteroid_disp():
    # Print asteroids to the screen

    for aster_i in range(len(list_asteroids)):
        x = int(list_asteroids[aster_i].pos_x)
        y = int(list_asteroids[aster_i].pos_y)
        r = list_asteroids[aster_i].radius_asteroid
        w = list_asteroids[aster_i].width
        pygame.draw.circle(DISPLAYSURF, WHITE, (x, y), r, w)


class Boss:
    # Boss asteroid

    def __init__(self, SW, SH):

        # Begining stats : positions
        self.radius = 30
        self.width = int(self.radius * 0.15)
        
        self.min_x = - self.radius
        self.max_x = SW + self.radius
        self.start_y = 0.285 * SH
        
        self.vel_x = 1/1200 * SH

        # Define position
        self.pos_x = self.min_x
        self.pos_y = self.start_y

        # Life point stats
        self.alive = True
        self.lifePoints = 20

        # Behaviour stats
        self.rest = False
        self.phase = 'right'

    def trajectory(self, x, SW, SH):
        y = (0.76 * SH) / (SW ** 2) * (x ** 2) - (0.76 * SH * x) / SW + 0.285 * SH
        return y

    def update_pos(self, SW, SH):
        # for boss from left to right
        if self.phase == 'right':
            self.pos_x += self.vel_x
            self.pos_y = self.trajectory(self.pos_x, SW, SH)
            if self.pos_x >= self.max_x:
                self.phase = 'left'
                self.rest = True

                self.pos_x = self.max_x
                self.pos_y = self.start_y

        #for boss from right to left
        elif self.phase == 'left':
            self.pos_x -= self.vel_x
            self.pos_y = self.trajectory(self.pos_x, SW, SH)
            if self.pos_x <= self.min_x:
                self.phase = 'right'
                self.rest = True
                
                self.pos_x = self.min_x
                self.pos_y = self.start_y


def boss_disp():
    """ Print on the screen the boss """

    x = int(BOSS.pos_x)
    y = int(BOSS.pos_y)
    r = BOSS.radius
    w = BOSS.width
    pygame.draw.circle(DISPLAYSURF, WHITE, (x,y), r, w)
    return x, y


def in_zone():
    """ Check if BOSS is in the correct zone to create a child
    return True if yes, False otherwise """

    return (BOSS.pos_x < (0.938 * SCREEN_WIDTH)) and (BOSS.pos_x > (0.071 * SCREEN_HEIGHT))


def boss_child_gen():
    """ Generate 1 asteroid at the SCREEN_WIDTH of BOSS """

    speed = (random.random() * 3) + 14.0
    size  = (random.randint(1, 4))
    aster = Asteroid(size, speed, BOSS.pos_x - 10, BOSS.pos_y + 10)
    
    list_asteroids.append(aster)

    return 1


def end_of_game(): # needs to be edited; score missing
    """ Last screen with :
    - score
    - time spent on game
    - option to go back to menu """
    if life_length == 0:
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(loss_surf, (((SCREEN_WIDTH - loss_surf.get_width()) // 2), (SCREEN_HEIGHT - loss_surf.get_height()) // 2))
        pygame.display.update()
        quit_game()

        # print loss screen
    elif not BOSS.alive:
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(win_surf, (((SCREEN_WIDTH - win_surf.get_width()) // 2), (SCREEN_HEIGHT - win_surf.get_height()) // 2))
        pygame.display.update()
        quit_game()
        # print win screen
    DISPLAYSURF.fill(BLACK)


def quit_game():
    time.sleep(10)
    pygame.quit()
    sys.exit()


def aim_pu():
    z1 = player.pos_x
    z2 = player.pos_y
    for z in range(SCREEN_HEIGHT):
        if z % 2 == 0:
            pygame.draw.line(DISPLAYSURF, RED, (z1, z2), (z1, z2-z))
        z2 = z2 - z


def laser_power_up(score):
    z1 = player.pos_x
    z2 = player.pos_y
    z3 = player.vel
    player.pos_x = SCREEN_WIDTH
    player.vel = SCREEN_WIDTH // 200
    
    score = update_score('laser', score)
    
    wait = True
    while player.pos_x > 0:
        DISPLAYSURF.fill(BLACK)
        player.update_pos("left")
        pygame.draw.line(DISPLAYSURF, RED, (player.pos_x, player.pos_y), (player.pos_x, 0), SCREEN_WIDTH // 20)
        player.display(SCREEN_WIDTH, SCREEN_HEIGHT)
        pygame.draw.polygon(DISPLAYSURF, RED, ((0, player.pos_y + SCREEN_HEIGHT // 20), (SCREEN_WIDTH, player.pos_y + SCREEN_HEIGHT // 20), (SCREEN_WIDTH, SCREEN_HEIGHT), (0, SCREEN_HEIGHT)))
        asteroid_disp()
        pygame.display.update()
        if wait:
            time.sleep(0.5)
        wait=False
        fpsClock.tick(FPS)
        play_sound(super_laser_fire)
        for aster_i in list_asteroids:
            if (aster_i.pos_x < player.pos_x + SCREEN_WIDTH // 60) and (aster_i.pos_x > player.pos_x - SCREEN_WIDTH // 60) and(aster_i.pos_y < player.pos_y):
                print("aster removed")
                list_asteroids.remove(aster_i)
                play_sound(asteroid_breaks)
    player.pos_x = z1
    player.pos_y = z2
    player.vel = z3
    laser_available = False

    return score


def update_score(phase, score):
    """ Update score """
    if phase == 'sec':
        score += 50 / 120
    elif phase == 'hit':
        score += 250
    elif phase == 'hurt':
        score -= 1000
    elif phase == 'laser':
        score *= (1 - 0.2)

    if score < 0:
        score = 0

    return score

# -------------------------- #

BOSS = Boss(SCREEN_WIDTH, SCREEN_HEIGHT)
WAVE, nb_obj = 0, 0 #initialise WAVE and nb_obj (the number of objects [asteroids] per WAVE)
time_sec = 0.0
end = False

pygame.display.set_caption('Asteroids')
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# draws background
DISPLAYSURF.fill(BLACK)
speed = SCREEN_WIDTH // 400

player = Ship(SCREEN_WIDTH, SCREEN_HEIGHT, speed)##creates player
scope = False
lose_life = True
successful_hit = 0
ground_hit = 0
boss_hit = 0
bar_length = 0
total_boss_life = 100
total_life = 100


# plays background music
bg_music_start()

######################################################################################
while True:
    text_score = 'Score: ' + str(int(SCORE))
    score_Surf = font_Score.render(text_score, True, WHITE, BLACK)
    textRectObj = score_Surf.get_rect()
    textRectObj.topleft = (10, 10)

    DISPLAYSURF.fill(BLACK)
    DISPLAYSURF.blit(score_Surf, textRectObj)

    player.vel = speed
    # draws player
    player.display(SCREEN_WIDTH, SCREEN_HEIGHT)

    # Health Bar Depletion
    life_length = total_life - (ground_hit * 10)
    if life_length > 0:
        if life_length > 0.75 * total_life:
            COLOR = GREEN
        elif life_length > 0.5 * total_life:
            COLOR = ORANGE
        elif life_length > 0 * total_life:
            COLOR = RED
        # draws health bar
        pygame.draw.rect(DISPLAYSURF, COLOR, (player.pos_x - SCREEN_WIDTH // 35, player.pos_y + SCREEN_HEIGHT // 35, life_length, SCREEN_HEIGHT // 80))

    else:
        end_of_game()

    pygame.draw.polygon(DISPLAYSURF, RED, ((0, player.pos_y + SCREEN_HEIGHT // 20), (SCREEN_WIDTH, player.pos_y + SCREEN_HEIGHT // 20), (SCREEN_WIDTH, SCREEN_HEIGHT), (0, SCREEN_HEIGHT)))#draws base

    if scope:
        aim_pu()

    if player.pos_x <= 0:
        player.pos_x = SCREEN_WIDTH - 1

    if player.pos_x >= SCREEN_WIDTH:
        player.pos_x = 1

    if player.pos_y <= 0:
        player.pos_y = SCREEN_HEIGHT - 1

    if player.pos_y >= SCREEN_HEIGHT:
        player.pos_y = 1

    SCORE = update_score('sec', SCORE)

    hits, SCORE = collision(list_bullets,list_asteroids, SCORE)  # checks for collisions between bullets and asteroids
    successful_hit += hits

    gr_hit, SCORE = ground_collision(list_asteroids, SCORE)  # checks for collisions with asteroid and base
    ground_hit += gr_hit 

    del_bullet(list_bullets)  # deletes stray bullets
    bullet_disp()  # displays bullets
    asteroid_disp()  # displays asteroids
    boss_disp()  # displays boss
    boss_x, boss_y = boss_disp()

    boss_hit += boss_collision(list_bullets,boss_x,boss_y)  # checks for an attack on boss

    key_i = pygame.key.get_pressed()  # returns a list storing true if a key is pressed and false if not pressed for all keys
    if speed_up:      
        player.vel = speed * 3

    if key_i[K_RIGHT]:
        player.update_pos("right")

    if key_i[K_LEFT]:
        player.update_pos("left")

    for event in pygame.event.get():
        
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if len(list_bullets) <= 4:
                    gen_bullet(player.pos_x, player.pos_y)

            if event.key == K_l:
                SCORE = laser_power_up(SCORE)

            if event.key == K_s:
                scope = not scope

            if event.key == K_LCTRL or event.key == K_RCTRL:
                speed_up = not speed_up

        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

    if WAVE < NUMBER_OF_WAVES:
        # waves 1 to 5
        if nb_obj < (WAVE * 5 + 5):
            # increases rate of generation of asteroids
            if time_sec >= (5 - WAVE):
                nb_obj += asteroid_gen()
                time_sec = 0.0
        else:
            if len(list_asteroids) == 0:
                WAVE += 1
                nb_obj = 0
                time_sec = 0.0
                
    elif BOSS.alive: #  implicit WAVE == 5
        #  waves 6 with BOSS
        if not BOSS.rest:
            BOSS.update_pos(SCREEN_WIDTH, SCREEN_HEIGHT)
            boss_life_tracker(total_boss_life, boss_hit, boss_x,boss_y)
            if time_sec >= 5 and in_zone():
                list_ = [1, 0, 0, 0, 0]
                if random.choice(list_):
                    boss_child_gen()
        if time_sec >= 5:
            nb_obj += asteroid_gen()
            time_sec = 0.0

    else:
        # after wave 6 : stop game
        end_of_game()

    for aster_i in range(len(list_asteroids)):
        list_asteroids[aster_i].update_pos(1 / 60)

    time_sec += 1 / 60

    if end:
        end_of_game()

    pygame.display.update()
    fpsClock.tick(FPS)
