#Kruskal's algorithm

import random

import sys

import time

import RPi.GPIO as GPIO

from shiftio import shiftOut

import gpiozero





GPIO.setmode(GPIO.BCM)

GPIO.setup(17,GPIO.OUT)

GPIO.setup(27,GPIO.OUT)





v=[] #[col][row]

COL=0

ROW=0





class vertax:

    wall=True

    rank=0

    def __init__(self,c,r):

        self.row=r

        self.col=c

        self.group=self



p=vertax



def findan(x):

    if x.group!=x:

        x.group=findan(x.group)

    return x.group



def link(a,b):

    if a.rank>b.rank:

        b.group=a.group

    else:

        a.group=b.group

        if a.rank==b.rank:

            b.rank+=1



def union(a,b):

    link(findan(a),findan(b))







def init(col,row):

    for c in range(col):

        newcol=[]

        for r in range(row):

            newv=vertax(c,r)

            newcol.append(newv)

        v.append(newcol)

    v[0][0].wall=False

    v[col-1][row-1].wall=False

def findadj(ver):

    adj=[]

    try:

        if not v[ver.col+1][ver.row].wall:

            adj.append(v[ver.col+1][ver.row])

    except IndexError:

        pass

    try:

        nextrow=ver.row+1

        if not v[ver.col][ver.row+1].wall:

            adj.append(v[ver.col][ver.row+1])

    except IndexError:

        pass

    try:

        if ver.col-1>=0:

            if not v[ver.col-1][ver.row].wall:

                adj.append(v[ver.col-1][ver.row])

    except IndexError:

        pass

    try:

        if ver.row-1>=0:

            if not v[ver.col][ver.row-1].wall:

                adj.append(v[ver.col][ver.row-1])

    except IndexError:

        pass

    return adj



def isBreakable(adj):

    adjlist=[]

    count=[]

    for x in adj:

        if findan(x) not in adjlist:

            adjlist.append(findan(x))

            count.append(1)

        else:

            count[adjlist.index(findan(x))]+=1

    

    count.sort()

    if len(count)==1:

        if count==[1]:

            return True

        return False

    if len(count)==2:

        if count==[1,1]:

            return True

        return False

    elif len(count)==3:

        if count!=[1,1,2]:

            return True

        return False

    elif len(count)==4:

        return True



def generate(startcol,length):#length is how long the maze is from the starting column

    walls=[]

    for c in range(startcol,startcol+length):

        for r in range(ROW):

            walls.append(v[c][r])

    del walls[len(walls)-1]

    del walls[0]



    while len(walls)!=0:

        nextv=random.randrange(0,len(walls))

        

        adjpath=findadj(walls[nextv])

        if len(adjpath)==0:

            walls[nextv].wall=False

        # elif len(adjpath)==1:

        #     walls[nextv].wall=False

        #     union(walls[nextv],adjpath[0])

        else:

            if isBreakable(adjpath):

                for x in adjpath:

                    union(x,walls[nextv])

                walls[nextv].wall=False



        del walls[nextv]



def bfs(p):

    visited=[]



    q=[]

    q.append([p])



    while len(q)!=0:

        path=q.pop(0)

        visited.append(path[-1])

        if path[-1]==v[COL-1][ROW-1]:

            return path



        adj=findadj(path[-1])

        for x in adj:

            if x not in visited:

                new_path=list(path)

                new_path.append(x)

                q.append(new_path)

            







def move(cmd,p):

    if cmd=='L':

        if p.col-1>=0:

            if not v[p.col-1][p.row].wall:

                p=v[p.col-1][p.row]

    elif cmd=='R':

        if p.col+1<=COL-1:

            if not v[p.col+1][p.row].wall:

                p=v[p.col+1][p.row]

    elif cmd=='U':

        if p.row+1<=ROW-1:

            if not v[p.col][p.row+1].wall:

                p=v[p.col][p.row+1]

    elif cmd=='D':

        if p.row-1>=0:

            if not v[p.col][p.row-1].wall:

                p=v[p.col][p.row-1]

    

        



    return p



def printgrid():

    for r in range(ROW-1,-1,-1):

        for c in range(COL):

            if v[c][r]==p:

                print("P",end="")

            elif v[c][r]==v[0][0]:

                print("S",end="")

            elif v[c][r]==v[COL-1][ROW-1]:

                print("E",end="")

            elif v[c][r].wall:

                print("X",end="")

            else:

                print('.',end="")

        print()

        

def turnOnAt(col_bin,row,color):

    color_bin=0 #Green by default

    if color=="red":

        color_bin=1

    elif color=="orange":

        color_bin=2

        

    shiftOut(17,27,col_bin,((color_bin+1)<<2*row)^0b11111111)

    time.sleep(0.001)

    



def printOnMatrix():

    rows=[]

    player=[1,0]

    end=[1,0]

    for r in range(4):

        onerow=0

        for c in range(COL):

            if v[c][r].wall:

                onerow+=(1<<c)

            elif v[c][r]==p:

                player[0]=player[0]<<c

                player[1]=r

            elif v[c][r]==v[COL-1][ROW-1]:

                end[0]=end[0]<<c

                end[1]=r

        rows.append(onerow)

    for r in range(4):

        turnOnAt(rows[r],ROW-1-r,"red")

    turnOnAt(player[0],ROW-1-player[1],"green")

    turnOnAt(end[0],ROW-1-end[1],"orange")

def passAnimation(t):

    for x in range(2):

        shiftOut(17,27,0b11111111,0b01010101)

        time.sleep(0.1)

        shiftOut(17,27,0b11111111,0b10101010)

        time.sleep(0.1)

        shiftOut(17,27,0b11111111,0b00000000)

        time.sleep(0.1)

    

    score=t

    r=0

    rows=[]

    onerow=0

    while score>0: 

        onerow=(onerow<<1)+1

        if onerow==255:

            rows.append(onerow)

            onerow=0

            r+=1

        score-=1

        if score==0:

            rows.append(onerow)

    for x in range(3000):

        turnOnAt(rows[x%len(rows)],x%len(rows),"red")

            

    

    shiftOut(17,27,0b00000000,0b11111111)

    time.sleep(0.1)

def createMaze(col,row):

    global COL

    global ROW

    global v

    global p

    COL=col

    ROW=row

    v=[] #[col][row]



    init(COL,ROW)

    generate(0,COL)

    while findan(v[0][0])!=findan(v[COL-1][ROW-1]):

        v=[]

        init(COL,ROW)

        generate(0,COL)

    p=v[0][0]

    p.wall=False

    v[COL-1][ROW-1].wall=False

def run(u,r,d,l):

    global p

    #u=gpiozero.Button(5)

    #r=gpiozero.Button(6)

    #d=gpiozero.Button(13)

    #l=gpiozero.Button(19)

    printOnMatrix()



    starttime=time.time()

    while p!=v[COL-1][ROW-1]:

        up=False

        down=False

        left=False

        right=False

        hint=False

        while not u.is_pressed and not r.is_pressed and not d.is_pressed and not l.is_pressed:

            printOnMatrix()

            if u.is_pressed:

                up=True



            elif d.is_pressed:

                down=True

                

            elif l.is_pressed:

                left=True

                

            elif r.is_pressed:

                right=True

            while (u.is_pressed or d.is_pressed or r.is_pressed or l.is_pressed):

                printOnMatrix()

                if u.is_pressed and d.is_pressed and r.is_pressed and l.is_pressed:

                    path=bfs(p)

                    printOnMatrix()

                    turnOnAt(1<<path[1].col,ROW-1-path[1].row,"green")

                    time.sleep(0.001)

                    up=False

                    down=False

                    left=False

                    right=False

            if up or down or left or right:

                break

        if up:

            p=move("U",p)

        elif down:

            p=move("D",p)

        elif left:

            p=move("L",p)

        elif right:

            p=move("R",p)

        if p!=v[COL-1][ROW-1]:

            printOnMatrix()

        else:

            timeused=round(time.time()-starttime)

            passAnimation(timeused)

        



    #GPIO.cleanup()

    print("Success")

    print("Time used: "+str(timeused)+"s")

