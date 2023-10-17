import pygame
from random import randint
import sys
import math

pygame.init()


screen = pygame.display.set_mode((640, 360))
pygame.display.set_caption('ACO')
clock = pygame.time.Clock()

ants = []

class Ant:
    
    def __init__(self):
        self.position = [randint(140, 220), randint(280, 360)]
        self.angle = randint(0, 359) * (math.pi / 180)
        self.trail = []
        self.trail_type = 'no food'
        self.has_food = False
        self.body = pygame.Rect(self.position[1] - 3, self.position[0] - 3, 3, 3)
        self.red = randint(0,255)
        self.green = randint(0,255)
        self.blue = randint(0,255)

def make_ant(list_o_ants, num_o_ants):
    for i in range(num_o_ants):
        list_o_ants.append(Ant())
    
def update_position():
    
    for ant in ants:
        trail_amount = 50
        if len(ant.trail) >= trail_amount:
            ant.trail.pop(-1)
            ant.trail.insert(0, pygame.Rect(ant.position[1] - 3, ant.position[0] - 3, 3, 3))
        else:
            ant.trail.insert(0, pygame.Rect(ant.position[1] - 3, ant.position[0] - 3, 3, 3))
        
        ant.position[0] += 3 * (math.sin(ant.angle))
        ant.position[1] += 3 * (math.cos(ant.angle))
        if ant.position[0] <= 1:
            ant.position[0] = 1
            ant.angle = randint(0, 359) * (math.pi / 180)
        if ant.position[0] >= 359:
            ant.position[0] = 359
            ant.angle = randint(0, 359) * (math.pi / 180)
        if ant.position[1] <= 1:
            ant.position[1] = 1
            ant.angle = randint(0, 359) * (math.pi / 180)
        if ant.position[1] >= 639:
            ant.position[1] = 639
            ant.angle = randint(0, 359) * (math.pi / 180)
            
        ant.body = pygame.Rect(ant.position[1] - 3, ant.position[0] - 3, 3, 3)
        
        
        #Trails Dont Work
        other1 = ant.red/trail_amount
        o2 = ant.green/trail_amount
        o3 = ant.blue/trail_amount
        
        for position in ant.trail:
            trail_amount -= 1
            num = other1 * trail_amount
            num2 = o2 * trail_amount
            num3 = o3 * trail_amount
            pygame.draw.rect(screen, (num, num2, num3), position)
        
        pygame.draw.rect(screen, (255, 255, 255), ant.body)
        
    
make_ant(ants, 300)

while True:
    
    screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
           
            
    update_position()

    pygame.display.flip()
    
    pygame.display.update()
    clock.tick(60)