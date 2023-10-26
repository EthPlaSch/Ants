import pygame
from random import randint
import sys
import math

pygame.init()
WIDTH = 640
HEIGHT = 360
OFFSET = 25
SENSOR_RECT_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('ACO')
clock = pygame.time.Clock()

ants = []
food = []
trail_length = 75
clicked = False
colony = pygame.Rect(310, 170, 20, 20)

class Ant:
    
    def __init__(self):
        self.position = [WIDTH/2, HEIGHT/2]
        self.angle = math.radians(randint(0, 359))
        self.trail = []
        self.trail_colour = (3, 65, 181)
        self.has_food = False
        self.body = pygame.Rect(self.position[0] - 3, self.position[1] - 3, 3, 3)
        self.forward = [0,0]
        self.forward[0]= math.cos(self.angle)
        self.forward[1]= math.sin(self.angle)
        self.middle = pygame.Rect((self.position[0] - (SENSOR_RECT_SIZE / 2)) + self.forward[0] * OFFSET *1.5, (self.position[1] - (SENSOR_RECT_SIZE / 2)) + self.forward[1] * OFFSET * 1.5, SENSOR_RECT_SIZE, SENSOR_RECT_SIZE)
        self.left = pygame.Rect((self.position[0] - (SENSOR_RECT_SIZE / 2)) + math.cos(self.angle - math.pi/4) * OFFSET, (self.position[1] - (SENSOR_RECT_SIZE / 2)) + math.sin(self.angle - math.pi/4) * OFFSET, SENSOR_RECT_SIZE, (self.position[1] - (SENSOR_RECT_SIZE / 2)))
        self.right = pygame.Rect((self.position[0] - (SENSOR_RECT_SIZE / 2)) + math.cos(self.angle + math.pi/4) * OFFSET, (self.position[1] - (SENSOR_RECT_SIZE / 2)) + math.sin(self.angle + math.pi/4) * OFFSET, SENSOR_RECT_SIZE, (self.position[1] - (SENSOR_RECT_SIZE / 2)))

def make_ant(list_o_ants, num_o_ants):
    for i in range(num_o_ants):
        list_o_ants.append(Ant())
        
def aim_at_food(ant, item):
        
        x = item[0] - ant.position[0]
        y = item[1] - ant.position[1]
        
        
        print(f'Ant x: {int(ant.position[1])}, Ant y: {int(ant.position[0])} | Colony x: {int(colony[0])}, Colony y: {int(colony[1])}')
        
        angle = (math.atan(x / y))
        
        print(f'Angle: {(math.degrees(angle)) % 359}')
        
        ant.angle = math.radians((math.degrees(angle)) % 359)
    
def check_collisions(ant, colony):
    
    middle = 0
    left = 0
    right = 0
    
    for item in food:
        
        if ant.body.colliderect(item) and ant.has_food == False:
            food.remove(item)
            ant.angle = math.radians((math.degrees(ant.angle) - 180) % 359)
            ant.has_food = True
            ant.trail_colour = (238, 17, 61)
        #if ant.middle.colliderect(item) and ant.has_food == False:
            #aim_at_food(ant, item)
        #elif ant.left.colliderect(item) and ant.has_food == False:
            #aim_at_food(ant, item)
        #elif ant.left.colliderect(item) and ant.has_food == False:
            #aim_at_food(ant, item) 
        
    if ant.has_food == True:
        for ant_boi in ants:
            ant_boi.trail.reverse()
            for tail in ant_boi.trail:
                if tail[3] == False:
                    if ant.middle.colliderect(tail[0]):
                        middle = tail[4]
                    if ant.left.colliderect(tail[0]):
                        left = tail[4]
                    if ant.right.colliderect(tail[0]):
                        right = tail[4]
            ant_boi.trail.reverse()
                    
        if middle > left and middle > right:
            pass
        elif right > left:
            ant.angle = math.radians((math.degrees(ant.angle) + 20) % 359)
        elif left > right:
            ant.angle = math.radians((math.degrees(ant.angle) - 20) % 359)
            
    if ant.body.colliderect(colony) and ant.has_food == True:
        ant.has_food = False
        ant.trail_colour = (3, 65, 181)
    
def update_position(ant):
    
    if len(ant.trail) >= trail_length:
        ant.trail.pop(-1)
        ant.trail.insert(0, [pygame.Rect(ant.position[0] - 3, ant.position[1] - 3, 3, 3), ant.angle, ant.trail_colour, ant.has_food, 255])
    else:
        ant.trail.insert(0, [pygame.Rect(ant.position[0] - 3, ant.position[1] - 3, 3, 3), ant.angle, ant.trail_colour, ant.has_food, 255])
    
    ant.position[0] += 2.5 * ant.forward[0]
    ant.position[1] += 2.5 * ant.forward[1]
    
    if ant.position[1] <= 1:
        ant.position[1] = 1
        ant.angle = math.radians(randint(0, 359))
    if ant.position[1] >= 359:
        ant.position[1] = 359
        ant.angle = math.radians(randint(0, 359))
    if ant.position[0] <= 1:
        ant.position[0] = 1
        ant.angle = math.radians(randint(0, 359))
    if ant.position[0] >= 639:
        ant.position[0] = 639
        ant.angle = math.radians(randint(0, 359))
    ant.forward[0] = math.cos(ant.angle)
    ant.forward[1] = math.sin(ant.angle)
    left=[math.cos(ant.angle - (math.pi / 3)), math.sin(ant.angle - (math.pi/3))]
    right=[math.cos(ant.angle + (math.pi / 3)), math.sin(ant.angle + (math.pi/3))]
    ant.body = pygame.Rect(ant.position[0] - 3, ant.position[1] - 3, 3, 3)
    ant.middle = pygame.Rect((ant.position[0] - (SENSOR_RECT_SIZE/2)) + ant.forward[0] * OFFSET, (ant.position[1] - (SENSOR_RECT_SIZE/2)) + ant.forward[1] * OFFSET, SENSOR_RECT_SIZE, SENSOR_RECT_SIZE)
    ant.left = pygame.Rect((ant.position[0] - (SENSOR_RECT_SIZE/2)) + left[0] * OFFSET, (ant.position[1] - (SENSOR_RECT_SIZE/2)) + left[1] * OFFSET, SENSOR_RECT_SIZE, SENSOR_RECT_SIZE)
    ant.right = pygame.Rect((ant.position[0] - (SENSOR_RECT_SIZE/2)) + right[0] * OFFSET, (ant.position[1] - (SENSOR_RECT_SIZE/2)) + right[1] * OFFSET, SENSOR_RECT_SIZE, SENSOR_RECT_SIZE)
    # #Trails Dont Work
    alpha = 255
    alpha_reduce = 255/trail_length
    for position in ant.trail:
        alpha -= alpha_reduce
        position.pop(-1)
        position.append(alpha)
        s = pygame.Surface((position[0][2], position[0][3]))
        s.set_alpha(alpha)
        s.fill(position[2])
        screen.blit(s, (position[0][0], position[0][1]))
    
    pygame.draw.rect(screen, (255, 255,255), ant.body)
    pygame.draw.rect(screen, (200, 200, 200), ant.middle)
    pygame.draw.rect(screen, (200, 200, 200), ant.left)
    pygame.draw.rect(screen, (200, 200, 200), ant.right)
        
    
make_ant(ants, 20)

# Drawing the Food
def draw_food(mouse_pos):
    
    if mouse_pos[0] > 0 and mouse_pos[0] < 640 and mouse_pos[1] > 0 and mouse_pos[1] < 360:
        if len(food) >= 2000:
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