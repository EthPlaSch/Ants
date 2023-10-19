import pygame
from random import randint
import sys
import math

pygame.init()


screen = pygame.display.set_mode((640, 360))
pygame.display.set_caption('ACO')
clock = pygame.time.Clock()

ants = []
global food
food = []
trail_length = 100
clicked = False
colony = pygame.Rect(310, 170, 20, 20)

class Ant:
    
    def __init__(self):
        self.position = [randint(140, 220), randint(280, 360)]
        self.angle = math.radians(randint(0, 359))
        self.trail = []
        self.trail_colour = (3, 65, 181)
        self.has_food = False
        self.body = pygame.Rect(self.position[1] - 3, self.position[0] - 3, 3, 3)

def make_ant(list_o_ants, num_o_ants):
    for i in range(num_o_ants):
        list_o_ants.append(Ant())
        
#    def aim_at_colony(ant, colony):
        
#        y = (colony[1] + 10) - ant.position[0]
#        x = (colony[0] + 10) - ant.position[1]
#        
#        print(f'Ant x: {int(ant.position[1])}, Ant y: {int(ant.position[0])} | Colony x: {int(colony[0])}, Colony y: {int(colony[1])}')
#        
#        angle = (math.atan(x / y))
#        
#        print(f'Angle: {(math.degrees(angle) + 90) % 359}')
        
#        ant.angle = math.radians((math.degrees(angle) + 90) % 359)
    
def check_collisions(ant, colony):
    
    for item in food:
        if ant.body.colliderect(item) and ant.has_food == False:
            food.remove(item)
            ant.has_food = True
            ant.trail_colour = (238, 17, 61)
            
    if ant.body.colliderect(colony) and ant.has_food == True:
        ant.has_food = False
        ant.trail_colour = (3, 65, 181)
    
def update_position(ant):
    
    if len(ant.trail) >= trail_length:
        ant.trail.pop(-1)
        ant.trail.insert(0, [pygame.Rect(ant.position[1] - 3, ant.position[0] - 3, 3, 3), ant.angle, ant.trail_colour])
    else:
        ant.trail.insert(0, [pygame.Rect(ant.position[1] - 3, ant.position[0] - 3, 3, 3), ant.angle, ant.trail_colour])
    
    ant.position[0] += 2.5 * (math.sin(ant.angle))
    ant.position[1] += 2.5 * (math.cos(ant.angle))
    
    if ant.position[0] <= 1:
        ant.position[0] = 1
        ant.angle = math.radians(randint(0, 359))
    if ant.position[0] >= 359:
        ant.position[0] = 359
        ant.angle = math.radians(randint(0, 359))
    if ant.position[1] <= 1:
        ant.position[1] = 1
        ant.angle = math.radians(randint(0, 359))
    if ant.position[1] >= 639:
        ant.position[1] = 639
        ant.angle = math.radians(randint(0, 359))
        
    ant.body = pygame.Rect(ant.position[1] - 3, ant.position[0] - 3, 3, 3)
        
        
    # #Trails Dont Work
    alpha = 255
    alpha_reduce = 255/trail_length
    for position in ant.trail:
        alpha -= alpha_reduce
        s = pygame.Surface((position[0][2], position[0][3]))
        s.set_alpha(alpha)
        s.fill(position[2])
        screen.blit(s, (position[0][0], position[0][1]))
    
    pygame.draw.rect(screen, (255, 255,255), ant.body)
        
    
make_ant(ants, 100)

# Drawing the Food
def draw_food(mouse_pos):
    
    if mouse_pos[0] > 0 and mouse_pos[0] < 640 and mouse_pos[1] > 0 and mouse_pos[1] < 360:
        if len(food) >= 100:
            food.pop(-1)
            food.insert(0, pygame.Rect(mouse_pos[0] - 3, mouse_pos[1] - 3, 3, 3))
        else:
            food.insert(0, pygame.Rect(mouse_pos[0] - 3, mouse_pos[1] - 3, 3, 3))
    
while True:
    
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (244, 150, 78), colony, border_radius = 5)
    
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # add a food function that puts food in the screen where the mouse is and being clicked
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
           
    if clicked == True:
        draw_food(mouse_pos)
        
    for item in food:
        pygame.draw.rect(screen, (71, 209, 99), item)
        
    for ant in ants:
        update_position(ant)
        check_collisions(ant, colony)

    pygame.display.flip()
    
    pygame.display.update()
    clock.tick(60)