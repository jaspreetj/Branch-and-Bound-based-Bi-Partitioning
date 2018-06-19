from graphics import *
100

nodesn = 12
partition = [[0,1,2,3,4,11],[5,6,7,8,9,10]]
nets = [[3,5,8],[9,5,8],[10,5,8],[6,0,11],[4,0,11],[5,7],[0,2],[11,1],[8,0,11]]
point = {}


win = GraphWin('final solution', 640, 640)
# win.yUp() # right side up coordinates
win.setBackground('white')
message = Text(Point(win.getWidth()/2, 30), 'Circuit Name')
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
    for i in range(len(each)):
        if(i>0):
            first = point[each[i]]
            second = point[each[i-1]]
            Line(first, second).draw(win)
            
#[3,5,8]   

#message.setText('Click anywhere to quit') # change text message
win.getMouse()
win.close() 
