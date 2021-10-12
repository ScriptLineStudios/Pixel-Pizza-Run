import pygame
import sys
import random
import time

pygame.init()

#WINDOW_SIZE = (800, 600)
RED = (255, 0, 0)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
BLUE = (169, 248, 252)

clock = pygame.time.Clock()

WINDOW_SIZE = (800,600)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window

display = pygame.Surface((400,300)) # used as the surface for rendering, which is scaled

scroll = [0, 0]

font_small = pygame.font.Font('dpcomic.ttf', 32)
font_small_ = pygame.font.Font('dpcomic.ttf', 34)

pizza_bits_ = [pygame.image.load("pizza_bit_1.png"), pygame.image.load("pizza_bit_2.png"), pygame.image.load("pizza_bit_3.png"),
                  pygame.image.load("pizza_bit_4.png")]

bg = pygame.image.load("hill.png").convert()
bg.set_colorkey((255,255,255))

pizza_score = 0

cooldown_number = 25

pizza_bits = []

pygame.mixer.music.load('music.wav')
pygame.mixer.music.play(-1)

restart_text = font_small.render(f"CLICK SPACE TO RESTART", True, pygame.Color('black'))
restart_text_ = font_small_.render("", True, pygame.Color('black'))

for pizza in pizza_bits_:
      pizza_ = pygame.transform.scale(pizza, (8 ,8))
      pizza_bits.append(pizza_)

pizza_box = []

for image in range(3):
    image = pygame.image.load("customer" + str(image) + ".png").convert()
    image.set_colorkey((0,162,232))
    pizza_box.append(image)



class house_class(object):
      def __init__(self, x, y, width, height):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
      def main(self, display, scroll):
            pygame.draw.rect(display, GREEN, (self.x+scroll[0], self.y+scroll[1], self.width, self.height))




class particle(object):
    def __init__(self, x, y, x_vel, y_vel, radius, color, image):
        self.x = x 
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.gravity = 1
        self.radius = radius
        self.color = color
        self.lifetime = 20
        self.image = image
    def draw(self, display):
        self.lifetime -= 1
       # self.gravity -= 0.2
        self.x += self.x_vel * 0.3
        self.y += self.y_vel * 0.3
        
        if self.image != None:
            self.image.set_alpha(self.lifetime * 25)  # 0 is fully transparent and 255 fully opaque.
            display.blit(self.image, (int(self.x), int(self.y)))
        else:
            pygame.draw.circle(display, (128, 128, 128), (int(self.x), int(self.y)), self.radius)



class road_class(object):
      def __init__(self, x, y):
            self.x = x
            self.y = y
            self.image = pygame.image.load("road.png").convert()
      def main(self, display, scroll):
            display.blit(pygame.transform.scale(self.image, (128, 128)), (self.x+scroll[0], self.y+scroll[1]))

class pizza_class(object):
      def __init__(self, x, y):
            self.x = x
            self.y = y
            self.image = pygame.image.load("pizza.png").convert()
            self.image.set_colorkey((63, 72, 204))
            self.image = pygame.transform.scale(self.image, (32, 32))
            self.hitbox = pygame.Rect(self.x, self.y, 1, 1)
      def main(self, display):
            self.hitbox = pygame.Rect(self.x, self.y, 32, 32)
            display.blit(self.image, (self.x, self.y))
            
      

class player_class(object):
      def __init__(self, x, y, width, height):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.player_speed = 5
            self.hitbox = pygame.Rect(self.x, self.y, 32, 32)
            self.images = pizza_box
            self.animation_count = 0
            

      def check_input(self):
            self.hitbox = pygame.Rect(self.x, self.y+3, 40, 32)

            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP] and self.y > 154 and not game_over:
                  self.y -= 5 
            if keys[pygame.K_DOWN] and self.y < 229 and not game_over:
                  self.y += 5 
                  
      def main(self, display):
            if self.animation_count  >= 12:
                self.animation_count = 0

            if not game_over:
                  self.animation_count += 1
            display.blit(self.images[self.animation_count//6], (self.x, self.y))

            

            self.check_input()

bgs = []

bg_cooldown = 0

bgs.append([-200])
bgs.append([200])


game_over = False

def draw_game_window():
      global pizza_score, cooldown_number, bg_cooldown, game_over
      display.fill(BLUE)

      if bg_cooldown == 0:
            bgs.append([600])
            bg_cooldown = 75
      else:
            bg_cooldown -= 1

  
      for b in bgs:
            if not game_over:
                  b[0] -= 5 
            display.blit(bg, (b[0], 0))


      if game_over:
            score_text = font_small.render(f"SCORE: {pizza_score}", True, pygame.Color('black'))
            game_over_text = font_small.render("GAME OVER", True, pygame.Color('black'))
            display.blit(game_over_text, (50, 25))
            display.blit(restart_text, (50, 50))
            display.blit(score_text, (50, 75))




      for road_ in roads:
            road_.main(display, scroll)

            if not game_over:
                  road_.x -= 5 

            if road_.x <= -300:
                  roads.remove(road_)

      for p in particles:
            p.draw(display)


      for pizza_ in pizzas:
            pizza_.main(display)

            if not game_over:
                  pizza_.x -= 5 * dt


            if player.hitbox.colliderect(pizza_.hitbox):
                  pizza_score = pizza_score + 1
                  if str(pizza_score)[-1] == "0" and pizza_score != 0 and cooldown_number != 11:
                        cooldown_number = cooldown_number - 1
                  for i in range(7):
                        particles.append(particle(pizza_.x, pizza_.y, random.randrange(-20, 20), random.randrange(-20, 20), random.randrange(1, 5), (random.randrange(45, 57),0,0), random.choice(pizza_bits)))
                  pizzas.remove(pizza_)
            if pizza_.x <= 0:
                  game_over = True             
                  pizzas.remove(pizza_)
                  
      player.main(display)
      screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
      pygame.display.update()

      clock.tick(60)


      
roads = []
particles= []
for i in range(20):
      roads.append(road_class((i*100), 150))
pizzas = []
cooldown = 0
last_time = time.time()
player = player_class(100, 150, 32,32)
#house = house_class(200, 200, 64, 64)
road = road_class(400, 100)
road_cooldown = 0
dt = 1

while True:
      fps = font_small.render(str(int(clock.get_fps())), True, pygame.Color('white'))

      for event in pygame.event.get():
            if event.type == pygame.QUIT:
                  pygame.QUIT
                  quit()
                  sys.exit()

      keys = pygame.key.get_pressed()

      if keys[pygame.K_SPACE]:
            if game_over:
                  game_over = False
                  pizzas = []
                  cooldown_number = 25
                  pizza_score = 0
                  bg_cooldown = 0
                  bgs=[]
                  bgs.append([-200])
                  bgs.append([200])


      if cooldown == 0:
            pizzas.append(pizza_class(player.x + 400, random.randrange(150, 250)))
            cooldown = cooldown_number

      else:
            cooldown -= 1

      if road_cooldown == 0:
            roads.append(road_class(900, 150))
            road_cooldown = 20
      else:
            road_cooldown -= 1

      draw_game_window()

                  
