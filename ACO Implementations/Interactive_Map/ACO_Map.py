# Original Code from:
# Induraj. (February, 2023). Implementing Ant colony optimization in python- solving Traveling salesman problem. Medium.
# https://induraj2020.medium.com/implementation-of-ant-colony-optimization-using-python-solve-traveling-salesman-problem-9c14d3114475

# Importing Libraries
import numpy as np
import pygame
import sys
import time
from random import randint

# Intialising Pygame
pygame.init()

# Constants
WIDTH = 1280
HEIGHT = 720

# Variables
clicked = False
places = []
points = []
lines = []
times = []

# Setting up Pygame variables      
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('ACO')
clock = pygame.time.Clock()

# create a surface object, image is drawn on it.
map = pygame.image.load("Map.png").convert()
map = pygame.transform.scale(map, (WIDTH, HEIGHT))
solve_img = pygame.image.load("Button_to_Solve.png").convert()
solve_img = pygame.transform.scale(solve_img, (98, 64))
 
# Using blit to copy content from one surface to other
screen.blit(map, (0, 0))
screen.blit(solve_img, (WIDTH - 98, HEIGHT - 64))

# Calculating the distance between two cities
def distance(point1, point2):
    return np.sqrt(np.sum((point1 - point2)**2))

# Running the optimisation algorithm
def ant_colony_optimization(points, n_ants, n_iterations, alpha, beta, evaporation_rate, Q):
    
    # Variables
    start = time.perf_counter()
    n_points = len(points)
    pheromone = np.ones((n_points, n_points))
    best_path = None
    best_path_length = np.inf
    
    # Run this loop for the desired amount iterations
    for iteration in range(n_iterations):
        paths = []
        path_lengths = []
        
        # Run this loop for the number of ants - Calculates the ant's path between the cities
        for ant in range(n_ants):
            
            # Setting all points to not visited
            visited = [False]*n_points
            
            # Pick a random starting point
            current_point = np.random.randint(n_points)
            
            # Setting current point to visited
            visited[current_point] = True
            
            # Starting path
            path = [current_point]
            path_length = 0
            
            # While there are some cities the ant hasn't visited, move to the next city and lay down pheromones
            while False in visited:
                
                # Setting an array of unvisited points
                unvisited = np.where(np.logical_not(visited))[0]
                probabilities = np.zeros(len(unvisited))
                
                # For all the unvisited points loop over them and calculate the probability the ant will go there based the amount of pheromones and the proximity (closeness) of the town
                for i, unvisited_point in enumerate(unvisited):
                    # Alpha and beta are powers that allow the user to control how much the ant will care about the pheromone strength and path distance
                    probabilities[i] = pheromone[current_point, unvisited_point]**alpha / distance(points[current_point], points[unvisited_point])**beta
                
                # Dividing those values by the sum of all other probablities
                probabilities /= np.sum(probabilities)
                
                # Chosing the next unvisited city based on the calculated probability
                next_point = np.random.choice(unvisited, p=probabilities)
                
                # Add the next point to the path
                path.append(next_point)
                
                # Add the distance between the current point and the decided next point to the distance of this path
                path_length += distance(points[current_point], points[next_point])
                
                # Set the current city to visited
                visited[next_point] = True
                
                # Make your current point the next decided point (ant moves to the next city)
                current_point = next_point
                
                # Repeat this loop until all cities have been visited
            
            # Add the ants path to the list of paths
            paths.append(path)
            
            # Add the length of the path to the list of path lengths
            path_lengths.append(path_length)
            
            # If the ant's path is shorter than the current best path, make the ant's path the new best path
            if path_length < best_path_length:
                best_path = path
                best_path_length = path_length
        
        # Evaportate (reduce the amount) the pheromones a little
        pheromone *= evaporation_rate
        
        # Looping over all the edges and adding the pheromones based on a constant divided by the distance of the path
        for path, path_length in zip(paths, path_lengths):
            for i in range(n_points-1):
                # To a particular edge along the path, find the current amount of pheromones on that path, then add some pheromones based on a constant divided by the distance from the current point to the next point
                pheromone[path[i], path[i+1]] += Q/path_length
            pheromone[path[-1], path[0]] += Q/path_length
     
    # return the best path and the list of points       
    return (best_path, points.tolist())

# Drawing the Food
def draw_food(mouse_pos):
    
    # Based on where the mouse is, and if the button is clicked, draw food
    if mouse_pos[0] > 0 and mouse_pos[0] < WIDTH and mouse_pos[1] > 0 and mouse_pos[1] < HEIGHT:
        
        # Capping number of cities at 500
        if len(places) >= 500:
            
            # Removing the oldest city from the list
            places.pop(-1)
            
            # Adding the position as a city to the list of cities
            points.insert(0, [mouse_pos[0], mouse_pos[1]])
        else:
            # Adding the position as a city to the list of cities
            points.insert(0, [mouse_pos[0], mouse_pos[1]])
   
# Calculating the lines for the solution         
def draw_solution(best_path, points):
    
    # Adding the best path order to the list of points
    for i in range(len(best_path)):
        points[best_path[i]].append(i)
        
    # Sorting the list of points into the order of the best path
    points.sort(key=lambda points: points[2])
    
    # Removing the best path index on the end of each path so it isn't annoying later
    for i in range(len(points)):
        points[i] = [points[i][0], points[i][1]]
        
    # Looping over the points and adding the start and end position for each line
    for i in range(len(points)):
        
        # Preventing a list index error by looping back to the start if you've reached the end of the list
        if i < (len(points) - 1):
            # Adding the start and end position for each line
            lines.append([points[i], points[(i + 1)]])
        else:
            # Adding the start and end position for each line
            lines.append([points[i], points[0]])
 
# Main simulation loop  
def main(clicked): 
    
    # 'Game' / Simulation Loop
    while True:
        
        # Drawing the map and button to the screen
        screen.blit(map, (0, 0))
        screen.blit(solve_img, (WIDTH - 98, HEIGHT - 64))

        # Getting the mouse position
        mouse_pos = pygame.mouse.get_pos()
        
        # Checking for inputs, namely quit and the mouse button
        for event in pygame.event.get():
            
            # Mouse button pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                # If the mouse is over the solve button
                if mouse_pos[0] > (WIDTH - 98) and mouse_pos[1] > (HEIGHT - 64):
                    
                    # Being able to access lines
                    global lines
                    
                    # Making lines blank
                    lines = []
                    
                    print('Solving...')
                    
                    # Running the ACO algorithm
                    a, b = ant_colony_optimization(np.array(points), n_ants=5, n_iterations=25, alpha=4, beta=8, evaporation_rate=0.8, Q=5)
                    
                    # Calling draw solution to calculate where the connecting lines are in the order the algorithm came up with
                    draw_solution(a, b)
                    print('Done!')
                  
                # If the mouse is anywhere else on the screen  
                else:
                    
                    # Call the draw food function to draw food to the screen
                    draw_food(mouse_pos)
                 
            # Close button pressed   
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # If there are any points on screen
        if points:    
            for place in points:
                # Drawing the food to the screen
                pygame.draw.circle(screen, (255, 41, 97), place, 7)
        
            
        for line in lines:
            # Drawing the lines connecting the nodes to the screen
            pygame.draw.line(screen, (255, 41, 97), line[0], line[1], 3)
            

        # Updating the whole screen
        pygame.display.flip()
        
        # Locking the frame rate at 60
        clock.tick(60)
      
# Typical Python practice
if __name__ == '__main__':
    main(clicked)