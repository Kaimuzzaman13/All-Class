"""
A* algorithm solves the N number problem
give the initial matrix and target matrix during the codes or from the keyboard

        Please enter the number of rows in the matrix
        
        3                           the number of N
        
        Please input the initial matrix A               
        
        1 0 2                      Input each line one by one, separated by Spaces, and enter the second line when the last number of each line is complete
        4 5 6
        3 7 8

        Please input the target matrix B
        1 2 3
        8 0 4
        7 6 5
"""
import numpy as np
import copy
import time
from operator import itemgetter

goal = {}

def get_location(vec, num):    #Gets the position of num in the matrix based on the num element
    row_num = vec.shape[0]     #numpy-shape gets the dimension of the matrix
    line_num = vec.shape[1]
    
    for i in range(row_num):
        for j in range(line_num):
            if num == vec[i][j]:
                return i, j

def get_actions(vec):    #Gets the next position that the current position can move, returning the move list
    row_num = vec.shape[0]
    line_num = vec.shape[1]
    
    (x, y) = get_location(vec, 0)    #Gets the location of the 0 element
    action = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    if x == 0:    #If 0 is on the edge, reduce the movable position of 0 depending on the position
        action.remove((-1, 0))
    if y == 0:
        action.remove((0, -1))
    if x == row_num - 1:
        action.remove((1, 0))
    if y == line_num - 1:
        action.remove((0, 1))
        
    return list(action)

def result(vec, action):    #Move the element, do the matrix transformation
     (x, y) = get_location(vec, 0)    #Gets the location of the 0 element
     (a, b) = action    #Gets the removable location
                                 
     n = vec[x+a][y+b]    #Move positions, swap elements
     s = copy.deepcopy(vec)
     s[x+a][y+b] = 0
     s[x][y] = n
     
     return s
    
def get_ManhattanDis(vec1, vec2):    #Manhattan distance of two matrices is calculated. Vec1 is the target matrix and Vec2 is the current matrix
    row_num = vec1.shape[0]
    line_num = vec1.shape[1]
    dis  = 0
    
    for i in range(row_num):
        for j in range(line_num):
            if vec1[i][j] != vec2[i][j] and vec2[i][j] != 0:
                k, m = get_location(vec1, vec2[i][j])
                d = abs(i - k) + abs(j - m)
                dis += d
                
    return dis

def expand(p, actions, step):           #Actions is the list of extensible states for the current matrix, P is the current matrix, and step is the number of steps taken
    children = []                                      #Use Children to save the extension node of the current state
    for action in actions:
        child = {}
        child['parent'] = p
        child['vec'] = (result(p['vec'], action))
        child['dis'] = get_ManhattanDis(goal['vec'], child['vec'])
        child['step'] = step + 1                       #The current traveled distance is increased by 1 for each extension
        child['dis'] = child['dis'] + child['step']    #Updates the value of f for this node  f=g+h（step+child[dis]）                     
        child['action'] = get_actions(child['vec'])
        children.append(child)
    
    return children

def node_sort(nodelist):    #Sort the list by the distance field of the dictionary of the node, from large to small
    return sorted(nodelist, key = itemgetter('dis'), reverse=True)

def get_input(num):
    A = []
    for i in range(num):
        temp = []
        p = []
        s = input()
        temp = s.split(' ')
        for t in temp:
            t = int(t)
            p.append(t)
        A.append(p)
   
    return A  

def get_parent(node):
    q = {}
    q = node['parent']   
    return q
        
def test():
    openlist = []    #open list
    close = []       #Store the parent nodes of the extension
    
    print('Please enter the number of rows of the matrix')
    #num = int(input())  
    num=3;
    print("Please enter the initial matrix A")
    #A = get_input(num)
    A=np.mat('1 0 2;4 5 6;3 7 8')

    print("Please enter the target matrix B")
    #B = get_input(num)
    B=np.mat('1 2 3;8 0 4;7 6 5')
        
    print("Please enter the filename of the result")
    #resultfile = input()
    resultfile = "a.txt"    
    goal['vec'] = np.array(B)   #Establish a matrix
   
    p = {}
    p['vec'] = np.array(A)
    p['dis'] = get_ManhattanDis(goal['vec'], p['vec'])
    p['step'] = 0
    p['action'] = get_actions(p['vec'])
    p['parent'] = {}

    if (p['vec'] == goal['vec']).all():
        return
    
    openlist.append(p)
    
    #start_CPU = time.clock()    #The CPU starts computing when the expansion begins
    
    while openlist:
        
        children = []
        
        node = openlist.pop()    #Node is a dictionary type and pops out the last element of the open list
        close.append(node)  #put it in the close list
      
        if (node['vec'] == goal['vec']).all():    #Compare the current and target matrices to check whether they are the same or not
            #end_CPU = time.clock()    #CPU finish calculation
         
            h = open(resultfile,'w',encoding='utf-8',)  #Write the results to a file and output them on the console
            h.write('Size of the search tree:' + str(len(openlist)+len(close)) + '\n')
            h.write('close：' + str(len(close)) + '\n')
            h.write('openlist：' + str(len(openlist)) + '\n')
            #h.write('CPU running time：' + str(end_CPU - start_CPU) + '\n')
            h.write('The path length:' + str(node['dis']) + '\n')
            
            h.write('The path of the solution: ' + '\n')
            i = 0
            way = []
            while close:
                way.append(node['vec'])  #The parent node is stored in the Way list by tracing up from the final state
                node = get_parent(node)
                if(node['vec'] == p['vec']).all():
                    way.append(node['vec'])
                    break
            while way:
                i += 1
                h.write(str(i) + '\n')
                h.write(str(way.pop()) + '\n')
            h.close()
            f = open(resultfile,'r',encoding='utf-8',)
            print(f.read())
            
            return
        
        children = expand(node, node['action'], node['step'])    #If it is not the target matrix, extend the current node and take the possible transition of the matrix

        for child in children:    
            f = False
            flag = False
            j = 0
            for i in range(len(openlist)):
                if (child['vec'] == openlist[i]['vec']).all():
                    j = i
                    flag = True
                    break
            for i in range(len(close)): #Discard it if it is in the close list
                if(child['vec'] == close[i]).all():
                    f = True
                    break
            if  f == False and flag == False :# Insert the open table if the new node is not in either the close table or the Open table
                openlist.append(child)
                
            elif flag == True: #compare the f values of the two matrices in the open list, and leave the smaller one in the open list
                if child['dis'] < openlist[j]['dis']:
                    del openlist[j]
                    openlist.append(child)
                    
        
        openlist = node_sort(openlist)   #Sort the Open list from large to small
    
test()
