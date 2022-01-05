
import operator

__metaclass__ = type
 
M = int(input("Please enter the number of missionaries："))  # missionaries
C = int(input("Please enter the number of savages:"))  # savages
K = int(input("Please enter the maximum capacity of the ship："))
# Number of passengers per boat
child = []  # child：To store all extension nodes
open_list = []  # open label
closed_list = []  # closed label
 
 
class State:
    def __init__(self, m, c, b):
        self.m = m  #Number of missionaries on the Left Bank
        self.c = c  #Number of left Bank savages
        self.b = b  # b = 1: The ship left bank；b = 0: The ship on the right bank
        self.g = 0
        self.f = 0  #f = g+h
        self.father = None
        self.node = [m, c, b]
 
init = State(M, C, 1)  # The initial node
goal = State(0, 0, 0)  # The target
 
#0 ≤ m ≤ 3,0 ≤ c ≤ 3, b ∈ {0,1}, On the left bank m > c(m is not 0), On the right bank 3-m > 3-c(m is not 3)
def safe(s):
    if s.m > M or s.m < 0 or s.c > C or s.c < 0 or (s.m != 0 and s.m < s.c) or (s.m != M and M - s.m < C - s.c):
        return False
    else:
        return True
 
 
# Inspired by the function
def h(s):
    return s.m + s.c - K * s.b
    # return M - s.m + C - s.c
 
def equal(a, b):
    if a.node == b.node:
        return 1,b
    else:
        return 0,b
 
# Determines whether the current state is consistent with the parent state
def back(new, s):
    if s.father is None:
        return False
    #Determines whether the current state is consistent with the ancestor state
    c=b=s.father
    while(1):
        a,c=equal(new, b)
        if a:
            return True
        b=c.father
        if b is None:
            return False
#make  open_list  Sort by f value
def open_sort(l):
    the_key = operator.attrgetter('f')  # Specifies the key to sort the property
    l.sort(key=the_key)
 
 
# When extending a node, look in open and closed tables for nodes that already have the same MCB attributes
def in_list(new, l):
    for item in l:
        if new.node == item.node:
            return True, item
    return False, None
 
 
def A_star(s):
    A=[]
    global open_list, closed_list
    open_list = [s]
    closed_list = []
    #print(len(open_list))
    # print （'closed list:'）  # Select print open table or Closed table change procedure
    #print(s.node)
    #a=1
    while(1):  # The open list is not empty
        #get = open_list[0]  # Fetch the first element of the open table, get
        for i in open_list:
            if i.node == goal.node:  # Determine if it is a target node
                A.append(i)
                open_list.remove(i)
        if not(open_list):
            break
        get=open_list[0]
        open_list.remove(get)  # Remove the GET from the Open table
        closed_list.append(get)  # Add GET to the Closed table
 
        # The following gets a new child node of get and considers whether to put it into OpenList
        for i in range(M+1):  # Shipboard missionary
            for j in range(C+1):  # The boat savage
                # Illegal situation on board
                if i + j == 0 or i + j > K or (i != 0 and i < j):
                    continue
                #a=a+1
                if get.b == 1:  # The current ship is on the left bank. The next state counts the ship on the right bank
                    new = State(get.m - i, get.c - j, 0)
                    child.append(new)
                    #print(1)
                else:  # The current ship is on the right bank. The next state counts the ship on the left bank
                    new = State(get.m + i, get.c + j, 1)
                    child.append(new)
                    #print(2)
                #priority：not>and>ture。If the state is not secure or the node to be extended is in the same state as the parent of the current node.
                if not safe(new) or back(new, get):  # Status illegal or new reentry
                    child.pop()
                #If the node to be expanded meets the above conditions, set its father to the current node, calculate F, and sort open_list
                else:
                    new.father = get
                    new.g = get.g + 1  #The distance from the starting point
                    new.f = get.g + h(get)  # f = g + h

                    open_list.append(new)
                    #print(len(open_list))
                    open_sort(open_list)
        # Print open or closed tables
        #for o in open_list:
        # for o in closed_list:
            #print(o)
            #print(o.node)
           # print(o.father)
        #print(a)
    return(A)
                        
 
# Recursive print path
def printPath(f):
    if f is None:
        return
    printPath(f.father)
    #Notice the difference between the print() statement before and after a recursive call. In the back to achieve a flashback output
    print(f.node )
 
 
if __name__ == '__main__':
    print ('There are %d missionaries, %d savages, ship capacity :%d' % (M, C, K))
    final = A_star(init)
    print("There are {} schemes".format(len(final)))
    if final:
        for i in(final):
            print ('There is a solution, and the solution is ：')
            printPath(i)
    else:
        print ('There is no solution！')
