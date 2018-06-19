#Jaspreet Jhoja RECURSION BASED BB based Bi-PARTITIONING

import random, math, time
from math import *
from graphics import *



print("Branch and Bound based Bi-Partitioning")
files = ['cm82a.txt', 'con1.txt', 'z4ml.txt', 'cm138a.txt', 'cm150a.txt', 'cm162a.txt',
         'cc.txt', 'twocm.txt', 'ugly8.txt', 'ugly16.txt']


for i in range(len(files)):
    print('['+str(i)+']'+' - '+ files[i])
#select a file to run
choice = input("choose files to run")

for i in range(1):
#for choice in range(6,10):
    #EXTRACT DATA FROM NETLIST

    filename = files[int(choice)]

    print(filename)

    global nets, netsn, nodesn, best_val
    nets = []  #net details
    netsn = 0  #number of nets
    nodesn = 0 #number of nodes
    best_val = 0#best cost -minimum is best
    best_solution =[] #update this in while loop

    #function to read file
    def readfile(filename): 
        global netsn, nodesn, nets, best_val
        
        #split lines to read one by one
        lines = open(filename).read().splitlines()

        nets = []

        #iterate lines, extract number of nets and individual net nodes 
        for i in range(len(lines)):
            if(i==0):
                netsn = int(lines[0].split(' ')[1])  #extract number of nets
                nodesn = int(lines[i].split(' ')[0])  #extract number of nodes
                best_val = 2 * nodesn
                
            else:
                #separate the net details and put them in a list
                temp = list(filter(None,lines[i].split(' ')[1:]))
                if(len(temp)>0):
                    nets.append(temp)
        
    #run the read function
    readfile(filename)


    #function to calculate cost
    def calculate_cost(array):
        total_cost = 0
        for each in nets:
            each = list(map(int,each)) #convert the net arrays to integer arrays as nets are stored as strings
            #if a net has common elements with firt partition and second partition then add 1 to the cost
            if(len(list(set(each)&set(array[0])))>0 and len(list(set(each)&set(array[1])))>0):
                #if(len(set(each)&set(array[0]+array[1]))==len(each)):
                    total_cost = total_cost+1
        return total_cost



    #ARRAY  [[left],[right],[to place], cost]

    all_nodes = [i for i in range((nodesn))]+[None]

     #function to select the next node
    def next_node(current_node, total_nodes):
        if(current_node < total_nodes-1):
            return current_node+1
        elif(current_node == total_nodes-1):
            return None

    size_limit = nodesn/2 #partition size limit

    #[[],[]]
    count = 0 #keeps track of how many nodes were explored


    #function to select random colors for gui
    def channel_picker(value):
      if value is None:
        return random.random
      if isinstance(value, tuple):
        start, stop = value
        return lambda: random.random() * (stop - start) + start
      return lambda: value

    #function to show final partition
    def gui(circuit_name, partition):
        point = {} #stores nodes and corresponding coordinates 
        win = GraphWin('final solution', 640, 640) #define window size and title
        win.setBackground('white') #set background
        #shows circuit name 
        message = Text(Point(win.getWidth()/2, 30), circuit_name)
        message.setTextColor('red')
        message.setStyle('italic')
        message.setSize(20)
        message.draw(win)
        
        #draw drawing area
        rect1 = Rectangle(Point(10,50),Point(630,620))
        rect1.setFill('yellow')
        rect1.draw(win)

        #draw partition line
        bipart_line = Line(Point(320,50),Point(320,620))
        bipart_line.draw(win)
        bipart_line.setWidth(4)


        #left partition stays between y = 70 - 600 and x = 20 - 310
        #associate coordinates with nodes according to the partitions they are in
        #for left partition
        left = partition[0]
        lx = 290
        ly = 70
        ly_adder = (600-70)/len(left)
        for each in left:
            if(ly<=600):
                if(lx >20):
                    point[each] = Point(lx, ly)
                    ly = ly+ ly_adder
            elif(ly >600):
                ly = 70
                lx = lx - 20

        #for right partition
        right = partition[1]
        rx = 350
        ry = 70
        ry_adder = (600-70)/len(right)
        for each in right:
            if(ry<600):
                if(rx < 620):
                    point[each] = Point(rx, ry)
                    ry = ry+ ry_adder
            if(ry >=600):
                ry = 70
                rx = rx + 20

        #draw all the nodes on the canvas
        for each in point:
            Circle(point[each], 5).draw(win)
            
        #draw lines between net nodes one by one
        for each in nets:
            each = list(map(int,each))
            for i in range(len(each)):
                if(i>0):
                    first = point[each[i]]
                    second = point[each[i-1]]
                    line = Line(first, second)
                    color = [channel_picker((0.1,225))() for _ in range(3)]
                    line.setFill(color_rgb(int(color[0]),int(color[1]), int(color[2])))
                    line.setWidth(5)
                    line.draw(win)
                    
        win.getMouse()
        win.close()

    #parition routine
    def routine( current_assignment, current_node, best_value):
        global best_solution, best_val, count

        #if reaches leaf then 
        if(current_node == None):
            print('leaf')
            print("best value: ",best_val, "current value: ", calculate_cost(current_assignment))
            #if current cost is lesser than best cost then accept it and update the best cost
            if(calculate_cost(current_assignment) < best_value):
                best_val = calculate_cost(current_assignment)
                best_solution = current_assignment
               # print(best_solution)

        else:
            temp_cost = calculate_cost(current_assignment)

            #if current cost is better than the best cost
            if(temp_cost<best_value):

                #check if we can place a node in left partition 
                go = False
                if(len(current_assignment[0]) < size_limit):
                    go = True
                if(len(current_assignment[0])== size_limit):
                    if(nodesn % 2 == 1):
                        if(len(current_assignment[0])+ size_limit < nodesn):
                            go = True

                
                #add a current node to the left partition and get next node
                #if next node  has better cost than best cost then expand it
                if(go == True):
                    count = count+1
                    #go left
                    temp_assignment = [current_assignment[0]+ [current_node], current_assignment[1]]
                    temp_next_node = next_node(current_node, nodesn)
                    if(calculate_cost(temp_assignment)<best_val):
                        routine(temp_assignment, temp_next_node, best_val)

                #check if we can place a node in the right partition
                go = False
                if(len(current_assignment[1]) < size_limit):
                    go = True
                if(len(current_assignment[1]) == size_limit):
                    if(nodesn%2 == 1):
                        if(size_limit+ len(current_assignment[1]) < nodesn):
                            go = True
                
                #go right
                #add current node to the right partition and get next node
                #if next node  has better cost than best cost then expand it
                if(go == True):
                    count = count+1
                    temp_assignment = [current_assignment[0], current_assignment[1]+ [current_node]]#[i for i in range(current_node, nodesn)]]
                    temp_next_node = next_node(current_node, nodesn)
                    if(calculate_cost(temp_assignment)<best_val):
                        routine(temp_assignment, temp_next_node, best_val)

    now = time.time() 
    routine([[],[]], 0, best_val)
    later = time.time()
    diff = later-now #total time taken in seconds
    print(diff)
    print("BEST VALUE: ", best_val)
    print("BEST SOLUTION", best_solution)
    gui(filename, best_solution)
