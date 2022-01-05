# -*- coding: utf-8 -*-
import random
import copy
import time
import sys
import math
import tkinter #//GUI module
import threading
from functools import reduce


# parameter
'''
Ant Colony Optimizatio
ALPHA:The greater the value of the information heuristic is, the more likely the ant will choose the path it has traveled before
       , the smaller the value is, the ant colony search range will be reduced, and it is easy to fall into the local optimal
BETA:The larger the Beta value is, the easier it is for the ant colony to choose a locally shorter path. In this case, 
      the convergence rate of the algorithm will be
     Speed up, but the randomness is not high, and is easy to get local relative optimal
'''

(ALPHA, BETA, RHO, Q) = (1.0,2.0,0.5,100.0)
# City number, ant colony
(city_num, ant_num) = (50,50)
distance_x = [
    178,272,176,171,650,499,267,703,408,437,491,74,532,
    416,626,42,271,359,163,508,229,576,147,560,35,714,
    757,517,64,314,675,690,391,628,87,240,705,699,258,
    428,614,36,360,482,666,597,209,201,492,294]
distance_y = [
    170,395,198,151,242,556,57,401,305,421,267,105,525,
    381,244,330,395,169,141,380,153,442,528,329,232,48,
    498,265,343,120,165,50,433,63,491,275,348,222,288,
    490,213,524,244,114,104,552,70,425,227,331]
#City distance and pheromones
distance_graph = [ [0.0 for col in range(city_num)] for raw in range(city_num)]
pheromone_graph = [ [1.0 for col in range(city_num)] for raw in range(city_num)]



#----------- ants -----------
class Ant(object):

    # Initialize
    def __init__(self,ID):
        
        self.ID = ID                 # ID
        self.__clean_data()          # Randomly initialize the points

    # The initial data
    def __clean_data(self):
    
        self.path = []               # The current ant's path
        self.total_distance = 0.0    # The total distance of the current path
        self.move_count = 0          # movement number
        self.current_city = -1       # Current city
        self.open_table_city = [True for i in range(city_num)] # Explore the states of the city
        
        city_index = random.randint(0,city_num-1) # Random initial points
        self.current_city = city_index
        self.path.append(city_index)
        self.open_table_city[city_index] = False
        self.move_count = 1
    
    # Choose the next city
    def __choice_next_city(self):
        
        next_city = -1
        select_citys_prob = [0.0 for i in range(city_num)]  #Store the probability of the next cities which will go
        total_prob = 0.0

        # Get the probability of the next city which will go
        for i in range(city_num):
            if self.open_table_city[i]:
                try :
                    # Calculated probability: proportional to the pheromone concentration and inversely proportional to the distance
                    select_citys_prob[i] = pow(pheromone_graph[self.current_city][i], ALPHA) * pow((1.0/distance_graph[self.current_city][i]), BETA)
                    total_prob += select_citys_prob[i]
                except ZeroDivisionError as e:
                    print ('Ant ID: {ID}, current city: {current}, target city: {target}'.format(ID = self.ID, current = self.current_city, target = i))
                    sys.exit(1)
        
        # Choose the city with Roulette
        if total_prob > 0.0:
            # Generate a random probability,0.0-total_prob
            temp_prob = random.uniform(0.0, total_prob)
            for i in range(city_num):
                if self.open_table_city[i]:
                    # Rounds by subtracting
                    temp_prob -= select_citys_prob[i]
                    if temp_prob < 0.0:
                        next_city = i
                        break

        # Select an unvisited city in order
        # if next_city == -1:
        #     for i in range(city_num):
        #         if self.open_table_city[i]:
        #             next_city = i
        #             break

        if (next_city == -1):
            next_city = random.randint(0, city_num - 1)
            while ((self.open_table_city[next_city]) == False):  # if==False,means it has been traversed
                next_city = random.randint(0, city_num - 1)

        # Returns number of next city
        return next_city
    
    # Calculate total distance of the path
    def __cal_total_distance(self):
        
        temp_distance = 0.0

        for i in range(1, city_num):
            start, end = self.path[i], self.path[i-1]
            temp_distance += distance_graph[start][end]

        # loop
        end = self.path[0]
        temp_distance += distance_graph[start][end]
        self.total_distance = temp_distance
        
    
    # Movement operating
    def __move(self, next_city):
        
        self.path.append(next_city)
        self.open_table_city[next_city] = False
        self.total_distance += distance_graph[self.current_city][next_city]
        self.current_city = next_city
        self.move_count += 1
        
    # Search the path
    def search_path(self):

        # Initialize the data
        self.__clean_data()

        # Search the path until you have traversed all the cities
        while self.move_count < city_num:
            # Move to the next city
            next_city =  self.__choice_next_city()
            self.__move(next_city)

        # Calculate the total path length
        self.__cal_total_distance()

#----------- The TSP problem -----------
        
class TSP(object):

    def __init__(self, root, width = 800, height = 600, n = city_num):

        # Create a canvas
        self.root = root                               
        self.width = width      
        self.height = height
        # The number of cities is initialized as city_num
        self.n = n
        # tkinter.Canvas
        self.canvas = tkinter.Canvas(
                root,
                width = self.width,
                height = self.height,
                bg = "#EBEBEB",             #The white background
                xscrollincrement = 1,
                yscrollincrement = 1
            )
        self.canvas.pack(expand = tkinter.YES, fill = tkinter.BOTH)
        self.title("TSP ant colony algorithm (N: initialization E: start searching S: stop searching Q: exit the program)")
        self.__r = 5
        self.__lock = threading.RLock()     # Thread lock

        self.__bindEvents()
        self.new()

        # Calculate the distance between cities
        for i in range(city_num):
            for j in range(city_num):
                temp_distance = pow((distance_x[i] - distance_x[j]), 2) + pow((distance_y[i] - distance_y[j]), 2)
                temp_distance = pow(temp_distance, 0.5)
                distance_graph[i][j] =float(int(temp_distance + 0.5))

    # Key responder
    def __bindEvents(self):

        self.root.bind("q", self.quite)        # Exit the program
        self.root.bind("n", self.new)          # Initialize
        self.root.bind("e", self.search_path)  # Begin your search
        self.root.bind("s", self.stop)         # Stop the search

    # Change the title
    def title(self, s):

        self.root.title(s)

    # Initialize
    def new(self, evt = None):

        # Stop the thread
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()

        self.clear()     # Clear information
        self.nodes = []  # The node coordinates
        self.nodes2 = [] # The node object

        # Initializes the city nodes
        for i in range(len(distance_x)):
            # Random initial coordinates on the canvas
            x = distance_x[i]
            y = distance_y[i]
            self.nodes.append((x, y))
            # Generate the node ellipse with radius self.__r
            node = self.canvas.create_oval(x - self.__r,
                    y - self.__r, x + self.__r, y + self.__r,
                    fill = "#ff0000",      # Fill in the red color
                    outline = "#000000",   # Outline with white color
                    tags = "node",
                )
            self.nodes2.append(node)
            # Display the coordinate
            self.canvas.create_text(x,y-10,              # Use the create_text method to draw text at (302,77)
                    text = '('+str(x)+','+str(y)+')',    # The contents will be drawn 
                    fill = 'black'                       # The drawn text is gray
                )
            
        # Connecting cities sequentially
        #self.line(range(city_num))
        
        # Distance and pheromones between the original cities
        for i in range(city_num):
            for j in range(city_num):
                pheromone_graph[i][j] = 1.0
                
        self.ants = [Ant(ID) for ID in range(ant_num)]  # The initial ant colony
        self.best_ant = Ant(-1)                          # Initial optimal solution
        self.best_ant.total_distance = 1 << 31           # Initial maximum distance
        self.iter = 1                                    #Initialize the number of iterations
            
    # Line the nodes in order
    def line(self, order):
        # Delete the original line
        self.canvas.delete("line")
        def line2(i1, i2):
            p1, p2 = self.nodes[i1], self.nodes[i2]
            self.canvas.create_line(p1, p2, fill = "#000000", tags = "line")
            return i2
        
        # order[-1] is the initial value
        reduce(line2, order, order[-1])

    # Remove the canvas
    def clear(self):
        for item in self.canvas.find_all():
            self.canvas.delete(item)

    # Exit the program
    def quite(self, evt):
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()
        self.root.destroy()
        print (u"\n Exist...")
        sys.exit()

    # Stop the search
    def stop(self, evt):
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()
        
    # Begin your search
    def search_path(self, evt = None):

        # Run the thread
        self.__lock.acquire()
        self.__running = True
        self.__lock.release()
        
        while self.__running:
            # Go through each ant
            for ant in self.ants:
                # Search for a path
                ant.search_path()
                # Compared with the current optimal ant
                if ant.total_distance < self.best_ant.total_distance:
                    # Update the optimal solution
                    self.best_ant = copy.deepcopy(ant)
            # Update pheromone
            self.__update_pheromone_gragh()
            print (u"The number of iterations：",self.iter,u" Optimal path total distance：",int(self.best_ant.total_distance))
            # attachment
            self.line(self.best_ant.path)
            # Set the title
            self.title("TSP(N: random initial E: start searching S: stop searching Q: exit the program) Iteration times: %d" % self.iter)
            # Update the canvas
            self.canvas.update()
            self.iter += 1

    # Update pheromone
    def __update_pheromone_gragh(self):

        # Get the pheromones left by each ant in its path
        temp_pheromone = [[0.0 for col in range(city_num)] for raw in range(city_num)]
        for ant in self.ants:
            for i in range(1,city_num):
                start, end = ant.path[i-1], ant.path[i]
                # Leaving a pheromone between every two adjacent cities on the path, inversely proportional to the total distance of the path
                temp_pheromone[start][end] += Q / ant.total_distance
                temp_pheromone[end][start] = temp_pheromone[start][end]

        # Update pheromone between all cities, decaying the old pheromone, plus the new iteration pheromone
        for i in range(city_num):
            for j in range(city_num):
                pheromone_graph[i][j] = pheromone_graph[i][j] * RHO + temp_pheromone[i][j]

    # The main loop
    def mainloop(self):
        self.root.mainloop()

#----------- The main program -----------
                
if __name__ == '__main__':


    TSP(tkinter.Tk()).mainloop()
