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
trail_length = 10

class Ant:
    
    def __init__(self):
        self.position = [randint(140, 220), randint(280, 360)]
        self.angle = randint(0, 359) * (math.pi / 180)
        self.trail = []
        self.trail_type = 'no food'
        self.has_food = False
        self.body = pygame.Rect(self.position[1] - 3, self.position[0] - 3, 3, 3)

def make_ant(list_o_ants, num_o_ants):
    for i in range(num_o_ants):
        list_o_ants.append(Ant())
    
def update_position():
    
    for ant in ants:
        
        if len(ant.trail) >= trail_length:
            ant.trail.pop(-1)
            ant.trail.insert(0, [pygame.Rect(ant.position[1] - 3, ant.position[0] - 3, 3, 3), ant.angle])
        else:
            ant.trail.insert(0, [pygame.Rect(ant.position[1] - 3, ant.position[0] - 3, 3, 3), ant.angle])
        
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
        
        
        # #Trails Dont Work
        alpha = 255
        alpha_reduce = 255/trail_length
        for position in ant.trail:
            alpha -= alpha_reduce
            s = pygame.Surface((position[0][2], position[0][3]))
            s.set_alpha(alpha)
            s.fill((255, 0, 255))
            screen.blit(s, (position[0][0], position[0][1]))
        
        pygame.draw.rect(screen, (255, 255,255), ant.body)
        
    
make_ant(ants, 500)

# Drawing the Food
def draw_food(mouse_pos):
    
    if mouse_pos[0] > 0 and mouse_pos[0] < 640 and mouse_pos[1] > 0 and mouse_pos[1] < 360:
        print('added food')
        if len(food) >= 100:
            food.pop(-1)
            food.insert(0, pygame.Rect(mouse_pos[0] - 3, mouse_pos[1] - 3, 3, 3))
        else:
            food.insert(0, pygame.Rect(mouse_pos[0] - 3, mouse_pos[1] - 3, 3, 3))
    

clicked = False

while True:
    
    screen.fill((0, 0, 0))
    
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
        print('Mouse Down')
        draw_food(mouse_pos)
        
    for item in food:
        pygame.draw.rect(screen, (255, 0, 0), item)
        
    update_position()

    pygame.display.flip()
    
    pygame.display.update()
    clock.tick(60)