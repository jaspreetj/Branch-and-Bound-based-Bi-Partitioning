#Jaspreet Jhoja RECURSION

import random,copy, statistics, timeit, threading, math, time
from math import *
import numpy as np
import matplotlib.pyplot as plt
import queue as Queue
from graphics import *

#ones that didnt work
#cm150a
#cc
#twocm

print("BB Partitioning")
files = ['cm82a.txt', 'con1.txt', 'z4ml.txt', 'cm138a.txt', 'cm150a.txt', 'cm162a.txt',
         'cc.txt', 'twocm.txt', 'ugly8.txt', 'ugly16.txt']


for i in range(len(files)):
    print('['+str(i)+']'+' - '+ files[i])

choice = input("choose files to run")


#EXTRACT DATA FROM NETLIST

filename = files[int(choice)]

#filename = 'ap.txt'

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



#CALCULATE COST
def calculate_cost(array):
    total_cost = 0
    for each in nets:
        each = list(map(int,each))
        if(len(list(set(each)&set(array[0])))>0 and len(list(set(each)&set(array[1])))>0):
            #if(len(set(each)&set(array[0]+array[1]))==len(each)):
                total_cost = total_cost+1
    return total_cost



#ARRAY  [[left],[right],[to place], cost]
#if we have explored 6/10 then it means it should goto right

all_nodes = [i for i in range((nodesn))]+[None]
jobs = []

def next_node(current_node, total_nodes):
    if(current_node < total_nodes-1):
        return current_node+1
    elif(current_node == total_nodes-1):
        return None

def channel_picker(value):
  if value is None:
    return random.random
  if isinstance(value, tuple):
    start, stop = value
    return lambda: random.random() * (stop - start) + start
  return lambda: value


def gui(circuit_name, partition):
    point = {}
    win = GraphWin('final solution', 640, 640)
    # win.yUp() # right side up coordinates
    win.setBackground('white')
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
    #place partition
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
    
    for each in point:
        Circle(point[each], 5).draw(win)
    #draw nets one by one
    for each in nets:
        each = list(map(int,each))
        color = [channel_picker((0.1,225))() for _ in range(3)]
        for i in range(len(each)):
            if(i>0):
              
                first = point[each[i]]
                second = point[each[i-1]]
                line = Line(first, second)
                
                line.setFill(color_rgb(int(color[0]),int(color[1]), int(color[2])))
                line.setWidth(5)
                line.draw(win)
                
    win.getMouse()
    win.close()


size_limit = nodesn/2

#[[[],[]], cost, node]
count = 0


#initial job
jobs.append([[[],[]], 0, 0])

closed = []
now = time.time()

while len(jobs)>0:

    #sort jobs    
    jobs = sorted(jobs, key=lambda x: x[1], reverse=True)


    #select job
    current = jobs[0]
    closed.append(current)
    
    jobs.pop(0)

    #evaluate it
    if(len(current[0][0]+current[0][1]) == nodesn):
            print('leaf')
            print("best value: ",best_val, "current value: ", calculate_cost(current[0]))
            if(calculate_cost(current[0]) < best_val):
                best_val = calculate_cost(current[0])
                best_solution = current[0]     

    #add to jobs
    else:
        temp_cost = calculate_cost(current[0])
        if(temp_cost < best_val):
            #if it has hope then generate left and right and add both to job roster
            assignment = current[0]
            count = count  + 1
            remainder =  nodesn - len(assignment[0]+assignment[1])
            left = 0
            right = 0
            #evaluate left
            if(len(assignment[0]) < size_limit):
                left = 1
            elif(len(assignment[0]) == size_limit):
                if(nodesn %2 == 1):
                    left = 1

            #evaluate right
            if(len(assignment[1]) < size_limit):
                right = 1
            elif(len(assignment[1]) == size_limit):
                if(nodesn %2 == 1):
                    right = 1
            
            #check if available in left
            if(left == 1):
                current_node = current[2]
                temp_assignment = [assignment[0]+ [current_node], assignment[1]]
                temp_next_node = next_node(current_node, nodesn)
                if(calculate_cost(temp_assignment)<best_val):
                   # if(len(closed)>0):
                   #     [print("REPEATING") for each in closed if set(each[0][0]) == set(temp_assignment[0]) and set(each[0][1]) == set(temp_assignment[1])]
                    jobs.append([temp_assignment, calculate_cost(temp_assignment), temp_next_node])
                    
            #check if available in right
            if(right == 1):
                current_node = current[2]
                temp_assignment = [assignment[0], assignment[1]+ [current_node]]
                temp_next_node = next_node(current_node, nodesn)
                if(calculate_cost(temp_assignment)<best_val):
                    jobs.append([temp_assignment, calculate_cost(temp_assignment), temp_next_node])

#[[[],[]], cost, node]


#routine([[],[]], 0, best_val)
later = time.time()
diff = later-now
print(diff)
print("BEST VALUE: ", best_val)
gui(files[int(choice)], best_solution)
