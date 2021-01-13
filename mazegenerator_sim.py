#Kruskal's algorithm
import random
import sys
import time

# seed = random.randrange(sys.maxsize)
# # seed=1846766320
# random.seed(seed)

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
        if p.col+1<=23:
            if not v[p.col+1][p.row].wall:
                p=v[p.col+1][p.row]
    elif cmd=='U':
        if p.row+1<=7:
            if not v[p.col][p.row+1].wall:
                p=v[p.col][p.row+1]
    elif cmd=='D':
        if p.row-1>=0:
            if not v[p.col][p.row-1].wall:
                p=v[p.col][p.row-1]
    elif cmd=="hint":
        hint=bfs(p)
        print(hint[1].col,hint[1].row)

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
def run():
    global p
    printgrid()

    starttime=time.time()
    while p!=v[COL-1][ROW-1]:
        p=move(input(),p)
        printgrid()


    print("Success")
    print("Time used: "+str(round(time.time()-starttime))+"s")

# createMaze(24,8)
# run()