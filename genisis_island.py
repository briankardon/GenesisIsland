import pygame
from random import randint
import sys
from MapTools import *
pygame.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
Clock=pygame.time.Clock()
width=1440
height=720
def goodrand(which,*args):
    if which=='randint':
        from random import randint
    if which=='choice':
        from random import choice
    ret=[]
    for bleh in range(len(args)):
        for blah in range(args[bleh][1]):
            ret.append(str(args[bleh][0]))
    do=choice(ret)
    if which=='randint':
        return int(do)
    else:
        return do
screen=pygame.display.set_mode((width, height))
board=[]
first=1
map=make_map((720,1440), blur_size=12, max_value=255, integer=True)
for bleh in range(72):
    board.append([])
    for bluh in range(36):
        dograss=4
        domountains=1
        dotrees=2
        dosheep=1
        dowater=2
        if map[bleh,bluh]>-1 and map[bleh,bluh]<51:
            dograss=4
            domountains=1
            dotrees=1
            dosheep=1
            dowater=1
        if map[bleh,bluh]>50 and map[bleh,bluh]<102:
            dograss=1
            domountains=4
            dotrees=1
            dosheep=1
            dowater=1
        if map[bleh,bluh]>101 and map[bleh,bluh]<153:
            dograss=1
            domountains=1
            dotrees=4
            dosheep=1
            dowater=1
        if map[bleh,bluh]>152 and map[bleh,bluh]<204:
            dograss=1
            domountains=1
            dotrees=1
            dosheep=4
            dowater=1
        if map[bleh,bluh]>203 and map[bleh,bluh]<256:
            dograss=1
            domountains=1
            dotrees=1
            dosheep=1
            dowater=4
        ##try:
        ##    if board[bleh][bluh-1]=='grass' or board[bleh][bluh+1]=='grass' or board[bleh+1][bluh]=='grass' or board[bleh-1][bluh]=='grass':
        ##        dograss=(5+999999999999999999999999999999999999999999999999999*98999999999999999999999999*999999999999999999999999)
        ##    if board[bleh][bluh-1]=='mountains' or board[bleh][bluh+1]=='mountains' or board[bleh+1][bluh]=='mountains' or board[bleh-1][bluh]=='mountains':
        ##        domountains=(2+999999999999999999999999999999999999999999999999999*98999999999999999999999999*999999999999999999999999)
        ##    if board[bleh][bluh-1]=='trees' or board[bleh][bluh+1]=='trees' or board[bleh+1][bluh]=='trees' or board[bleh-1][bluh]=='trees':
        ##        dotrees=(3+999999999999999999999999999999999999999999999999999*98999999999999999999999999*999999999999999999999999)
        ##    if board[bleh][bluh-1]=='sheep' or board[bleh][bluh+1]=='sheep' or board[bleh+1][bluh]=='sheep' or board[bleh-1][bluh]=='sheep':
        ##        dosheep=(2+999999999999999999999999999999999999999999999999999*98999999999999999999999999*999999999999999999999999)
        ##    if board[bleh][bluh-1]=='water' or board[bleh][bluh+1]=='water' or board[bleh+1][bluh]=='water' or board[bleh-1][bluh]=='water':
        ##        dowater=(3+999999999999999999999999999999999999999999999999999*98999999999999999999999999*999999999999999999999999)
        ##except IndexError:
        ##    pass
        board[bleh].append((randint(150,230),goodrand('choice',('grass',dograss),('mountains',domountains),('trees',dotrees),('sheep',dosheep),('water',dowater))))
yx=randint(1,72)
yy=randint(1,36)
cool=0
class Pathfinder:
    def __init__(self,board,x,y,mex,mey):
        self.open=[]
        self.path=[]
        self.board=board
        self.endx=x
        self.endy=y
        self.x=mex
        self.y=mey
    def makepath(self):
        move=self.path
        if self.x>self.endx:
            try:
                if self.board[self.x-1][self.x]=='grass':
                    self.path.append([self.x-1,self.y])
            except IndexError:
                pass
        else:
            try:
                if self.board[self.x+1][self.x]=='grass':
                    self.path.append([self.x+1,self.y])
            except IndexError:
                pass
        if self.y>self.endy:
            try:
                if self.board[self.y-1][self.y]=='grass':
                    self.path.append([self.x,self.y-1])
            except IndexError:
                pass
        else:
            try:
                if self.board[self.y+1][self.y]=='grass':
                    self.path.append([self.x,self.y+1])
            except IndexError:
                pass
    def move(self):
        if self.x>self.endx:
            for bleh in range(len(self.path)):
                for bluh in range(len(self.path[bleh])):
                    if self.path[bleh][bluh]==self.x-1:
                        self.x-=1
        else:
            for bleh in range(len(self.path)):
                for bluh in range(len(self.path[bleh])):
                    if self.path[bleh][bluh]==self.x+1:
                        self.x+=1
        if self.y>self.endy:
            for bleh in range(len(self.path)):
                for bluh in range(len(self.path[bleh])):
                    if self.path[bleh][bluh]==self.y-1:
                        self.y-=1
        else:
            for bleh in range(len(self.path)):
                for bluh in range(len(self.path[bleh])):
                    if self.path[bleh][bluh]==self.y+1:
                        self.y+=1
x,y=pygame.mouse.get_pos()
while True:
    try:
        dude.makepath()
        dude.move()
    except NameError:
        pass
    screen.fill('blue')
    pygame.mouse.set_visible(False)
    x,y=pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type==pygame.MOUSEBUTTONDOWN:
            dude=Pathfinder(board,x,y,yx,yy)
    key=pygame.key.get_pressed()
    if key[pygame.K_x]:
        pygame.quit()
        sys.exit()
    for bleh in range(len(board)):
        for bluh in range(len(board[bleh])):
            if board[bleh][bluh][1]!='water':
                pygame.draw.rect(screen,[0,board[bleh][bluh][0],0],(bleh*20,bluh*20,20,20))
            if board[bleh][bluh][1]=='mountains':
                pygame.draw.polygon(screen, 'gray', ((bleh*20,(bluh*20)+20),((bleh*20)+10,bluh*20),((bleh*20)+20,(bluh*20)+20),(bleh*20,(bluh*20)+20)))
            if board[bleh][bluh][1]=='trees':
                pygame.draw.line(screen,'brown',((bleh*20)+10,(bluh*20)+10),((bleh*20)+10,(bluh*20)+20),5)
                pygame.draw.rect(screen,[0,100,0],(bleh*20,bluh*20,20,10))
            if board[bleh][bluh][1]=='sheep':
                pygame.draw.rect(screen,'white',((bleh*20)+5,bluh*20,15,10))
                pygame.draw.rect(screen,'black',(bleh*20,bluh*20,5,5))
                pygame.draw.line(screen,'black',(bleh*20+6,bluh*20+10),(bleh*20+6,bluh*20+20),3)
                pygame.draw.line(screen,'black',(bleh*20+18,bluh*20+10),(bleh*20+18,bluh*20+20),3)
    pygame.draw.circle(screen,[255,100,100],(x,y),5)
    pygame.draw.circle(screen,'red',(yx*20-10,yy*20-10),10)
    pygame.draw.line(screen,'white',(yx*20-10,yy*20-10),(x,y),2)
    try:
        pygame.draw.circle(screen,'red',(dude.x*20,dude.y*20),10)
    except NameError:
        pass
    pygame.display.flip()
    Clock.tick(60)
