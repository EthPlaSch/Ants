# This just a side project to demonstrate the complexity of the algorithm.
# This project is incomplete but still a neat representation of the algorithm

# Importing libraries
import pygame
from random import randint
import sys
import math

# Intialising Pygame
pygame.init()

# Simulation Constants
WIDTH = 640
HEIGHT = 360
CELL_SIZE = 8
COLONY_SIZE = 30
TRAIL_LENGTH = 40
ANT_SPEED = 2.5
NUMBER_OF_ANTS = 50
OFFSET = 15
SENSOR_RECT_SIZE = 15

# Usinf these to optimise by chucking the map (NOT IMPLEMENTED YET)
ants_with_food = []
ants_without_food = []
sectors = []

# Setting up simulation variables
ants = []
food = []
clicked = False
colony = pygame.Rect(WIDTH / 2 - COLONY_SIZE / 2, HEIGHT / 2 - COLONY_SIZE / 2, COLONY_SIZE, COLONY_SIZE)
num_x_cells = round(WIDTH / CELL_SIZE)
num_y_cells = round(HEIGHT / CELL_SIZE)

# Creating the cells that will segment the screen for optimisation (to be implemented)
for i in range(num_y_cells):
    for j in range(num_x_cells):
        # 3rd Cell if for ants, add ants trails to that so you only have to check the 9 surrounding squares
        sectors.append([(j * CELL_SIZE + CELL_SIZE), (i * CELL_SIZE) + CELL_SIZE, []])
  
# Setting up Pygame variables      
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('ACO')
clock = pygame.time.Clock()


# The ant class
class Ant:
    
    # Setting up ant properties
    def __init__(self):
        
        # Basic ant position and rects as well as angle, trail, and food information
        self.position = [WIDTH/2, HEIGHT/2]
        self.angle = math.radians(randint(0, 359))
        self.trail = []
        self.trail_colour = (3, 65, 181)
        self.has_food = False
        self.body = pygame.Rect(self.position[0] - 3, self.position[1] - 3, 3, 3)
        
        # Setting the forward vector
        self.forward = [0,0]
        self.forward[0]= math.cos(self.angle)
        self.forward[1]= math.sin(self.angle)
        
        # Setting up the sensors in front of the ant
        self.middle = pygame.Rect((self.position[0] - (SENSOR_RECT_SIZE / 2)) + self.forward[0] * OFFSET *1.5, (self.position[1] - (SENSOR_RECT_SIZE / 2)) + self.forward[1] * OFFSET * 1.5, SENSOR_RECT_SIZE, SENSOR_RECT_SIZE)
        self.left = pygame.Rect((self.position[0] - (SENSOR_RECT_SIZE / 2)) + math.cos(self.angle - math.pi/4) * OFFSET, (self.position[1] - (SENSOR_RECT_SIZE / 2)) + math.sin(self.angle - math.pi/4) * OFFSET, SENSOR_RECT_SIZE, (self.position[1] - (SENSOR_RECT_SIZE / 2)))
        self.right = pygame.Rect((self.position[0] - (SENSOR_RECT_SIZE / 2)) + math.cos(self.angle + math.pi/4) * OFFSET, (self.position[1] - (SENSOR_RECT_SIZE / 2)) + math.sin(self.angle + math.pi/4) * OFFSET, SENSOR_RECT_SIZE, (self.position[1] - (SENSOR_RECT_SIZE / 2)))

# Function for making ants
def make_ant(list_o_ants, num_o_ants):
    for i in range(num_o_ants):
        list_o_ants.append(Ant())
 
# Making the ants       
make_ant(ants, NUMBER_OF_ANTS)
    
# Function that handles ant collisions and updates the ant's angle accordingly
def check_collisions(ant, colony):
    
    # Box collisions
    middle = 0
    left = 0
    right = 0
    
    # Checking if the ant is colliding with a piece of food (will optimise later to not check every piece of food just the ones close to the ant)
    for item in food:
        
        # Drawing the food to the screen
        pygame.draw.rect(screen, (71, 209, 99), item)
        
        # If the ant doesn't have food and collides with food, give it the food, delete the food from the screen, change the ant's trail colour
        if ant.body.colliderect(item) and ant.has_food == False:
            food.remove(item)
            ant.angle = math.radians((math.degrees(ant.angle) - 180) % 359)
            ant.has_food = True
            ant.trail_colour = (238, 17, 61)
            
        # Steering towards food if the ant doesn't have food
        if ant.has_food == False:
            if ant.middle.colliderect(item):
                pass
            elif ant.left.colliderect(item):
                # Change the ants angle to steer left
                ant.angle = math.radians((math.degrees(ant.angle) - 5) % 359)
            elif ant.right.colliderect(item):
                # Change the ants angle to steer right
                ant.angle = math.radians((math.degrees(ant.angle) + 5) % 359) 
                
                
    # If the ant does have food, steer towards the blue trails     
    if ant.has_food == True:
        # Steer towards colony if close  
        if ant.left.colliderect(colony):
            # Change the ants angle to steer left
            ant.angle = math.radians((math.degrees(ant.angle) - 15) % 359)
        elif ant.right.colliderect(colony):
            # Change the ants angle to steer right
            ant.angle = math.radians((math.degrees(ant.angle) + 15) % 359)  
        else:    
            # Looping over every ant and every trail in every ant to check collisions with trails
            for other_ant in ants:          
                for tail in other_ant.trail:
                    if tail[3] == False:
                        # Regisitering those collisions
                        if ant.middle.colliderect(tail[0]):
                            middle = tail[5]
                        if ant.left.colliderect(tail[0]):
                            left = tail[5]
                        if ant.right.colliderect(tail[0]):
                            right = tail[5]
    
    # If the ant doesn't have food, steer towards the red trails            
    else:
        # Looping over every ant and every trail in every ant to check collisions with trails
        for other_ant in ants:
                for tail in other_ant.trail:
                    if tail[3] == True:
                        # Regisitering those collisions
                        if ant.middle.colliderect(tail[0]):
                            middle = tail[5]
                        if ant.left.colliderect(tail[0]):
                            left = tail[5]
                        if ant.right.colliderect(tail[0]):
                            right = tail[5]
      
      
    # Steering the ant based on the concentration of pheromones          
    if middle > left and middle > right:
        pass
    elif right > left:
        # Change the ants angle to steer right
        ant.angle = math.radians((math.degrees(ant.angle) + 10) % 359)
    elif left > right:
        # Change the ants angle to steer left
        ant.angle = math.radians((math.degrees(ant.angle) - 10) % 359)
     
    # If ant collides with the colony and has food, drop off the food       
    if ant.body.colliderect(colony) and ant.has_food == True:
        
        # Set food to false
        ant.has_food = False
        
        # Change trail colour back to blue
        ant.trail_colour = (3, 65, 181)
        
        # Turn 180 degrees
        ant.angle = math.radians((math.degrees(ant.angle) - 180) % 359)
 
# The function for handling the ant's position and trail position   
def update_position(ant):
    
    # Adding to the trail of the ant and removing any completetly faded trails
    if len(ant.trail) >= TRAIL_LENGTH:
        # Removing the end of the trail
        ant.trail.pop(-1)
        # Adding the current position as the next spot in thr trail
        ant.trail.insert(0, [pygame.Rect(ant.position[0] - 3, ant.position[1] - 3, 3, 3), ant.angle, ant.trail_colour, ant.has_food, 0,255])
    else:
        # Adding the current position as the next spot in thr trail
        ant.trail.insert(0, [pygame.Rect(ant.position[0] - 3, ant.position[1] - 3, 3, 3), ant.angle, ant.trail_colour, ant.has_food, 0,255])
    
    # Moving the ant forward in the direction its facing
    ant.position[0] += ANT_SPEED * ant.forward[0]
    ant.position[1] += ANT_SPEED * ant.forward[1]
    
    # Keeping the ant in the screen, forcing it to pick a new direction if it hits the edge
    if ant.position[1] <= 1:
        
        # Setting the ants position to the edge and making it pick a new direction to travel in
        ant.position[1] = 1
        ant.angle = math.radians(randint(0, 359))
        
    if ant.position[1] >= (HEIGHT - 1):
        
        # Setting the ants position to the edge and making it pick a new direction to travel in
        ant.position[1] = (HEIGHT - 1)
        ant.angle = math.radians(randint(0, 359))
        
    if ant.position[0] <= 1:
        
        # Setting the ants position to the edge and making it pick a new direction to travel in
        ant.position[0] = 1
        ant.angle = math.radians(randint(0, 359))
        
    if ant.position[0] >= (WIDTH - 1):
        
        # Setting the ants position to the edge and making it pick a new direction to travel in
        ant.position[0] = (WIDTH - 1)
        ant.angle = math.radians(randint(0, 359))
        
    # Calculating the ant's forward vector
    ant.forward[0] = math.cos(ant.angle)
    ant.forward[1] = math.sin(ant.angle)
    
    # Calculating the position of the ant's sensors
    left=[math.cos(ant.angle - (math.pi / 2.5)), math.sin(ant.angle - (math.pi/2.5))]
    right=[math.cos(ant.angle + (math.pi / 2.5)), math.sin(ant.angle + (math.pi/2.5))]
    
    # Updating the rects for the ant's body and sensors
    ant.body = pygame.Rect(ant.position[0] - 3, ant.position[1] - 3, 3, 3)
    ant.middle = pygame.Rect((ant.position[0] - (SENSOR_RECT_SIZE/2)) + ant.forward[0] * OFFSET, (ant.position[1] - (SENSOR_RECT_SIZE/2)) + ant.forward[1] * OFFSET, SENSOR_RECT_SIZE, SENSOR_RECT_SIZE)
    ant.left = pygame.Rect((ant.position[0] - (SENSOR_RECT_SIZE/2)) + left[0] * OFFSET, (ant.position[1] - (SENSOR_RECT_SIZE/2)) + left[1] * OFFSET, SENSOR_RECT_SIZE, SENSOR_RECT_SIZE)
    ant.right = pygame.Rect((ant.position[0] - (SENSOR_RECT_SIZE/2)) + right[0] * OFFSET, (ant.position[1] - (SENSOR_RECT_SIZE/2)) + right[1] * OFFSET, SENSOR_RECT_SIZE, SENSOR_RECT_SIZE)

    # Giving the trails opacity
    alpha = 255
    alpha_reduce = 255/TRAIL_LENGTH
    
    # Reducing the opacity of the trail over time
    for position in ant.trail:
        alpha -= alpha_reduce
        
        # Removing the end of the trail
        position.pop(-1)
        position.append(alpha)
        
        # Drawing the trail to a surface
        s = pygame.Surface((position[0][2], position[0][3]))
        s.set_alpha(alpha)
        s.fill(position[2])
        screen.blit(s, (position[0][0], position[0][1]))
    
    # Drawing the ant body
    pygame.draw.rect(screen, (240, 240, 240), ant.body)

# Drawing the Food
def draw_food(mouse_pos):
    
    # Based on where the mouse is, and if the button is clicked, draw food
    if mouse_pos[0] > 0 and mouse_pos[0] < 640 and mouse_pos[1] > 0 and mouse_pos[1] < 360:
        # Capping the amount of food at 1000
        if len(food) >= 1000:
            
            # Removing the last piece of food
            food.pop(-1)
            # Adding a new piece of food to the list where the mouse is
            food.insert(0, pygame.Rect(mouse_pos[0] - 3, mouse_pos[1] - 3, 3, 3))
        else:
            # Adding a new piece of food to the list where the mouse is
            food.insert(0, pygame.Rect(mouse_pos[0] - 3, mouse_pos[1] - 3, 3, 3))
 
# Main simulation function
def main(clicked): 
    
    # Main simulation loop  
    while True:
        
        # Filling the screen with black
        screen.fill((0, 0, 0))
        
        # Drawing the colony
        pygame.draw.rect(screen, (244, 150, 78), colony, border_radius = 5)
        
        # Getting the mouse position
        mouse_pos = pygame.mouse.get_pos()
        
        # Checking for inputs, namely quit and the mouse button
        for event in pygame.event.get():
            
            # Checking for mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            # Checking for mouse button up
            if event.type == pygame.MOUSEBUTTONUP:
                clicked = False
            # Checking if the window is closed
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # If the mouse is down, call the draw food function to draw food      
        if clicked == True:
            draw_food(mouse_pos)
        
        # For every ant, update its position and check for collisions    
        for ant in ants:
            update_position(ant)
            check_collisions(ant, colony)

        # Updating the whole screen
        pygame.display.flip()
        
        # Locking the frame rate at 60
        clock.tick(60)
        
# Typical Python practice
if __name__ == '__main__':
    main(clicked)