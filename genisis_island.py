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

class Tile:
    size=20
    def __init__(self, tile_coord=(0, 0), biome='plains', grass_color=None):
        self.biome = biome
        self.entities = []
        self.resources = []
        self.image = None
        if grass_color is None:
            self.grass_color=randint(150,230)
        else:
            self.grass_color = grass_color
        self.tile_coord = tile_coord
        self.update_image()
        self.update_rect()

    def update_rect():
        tile_coords = [*self.tile_coords, 1, 1]
        coords = [coord * Tile.size for coord in tile_coords]
        self.rect = pygame.Rect(*coords)

    def update_image(self):
        s = Tile.size
        self.image = pygame.Surface((s, s))
        if self.biome == 'water':
            # Draw water background
            self.image.fill('blue')
        else:
            # Draw grass background
            self.image.fill([0, self.grass_color, 0])
        if self.biome == 'mountains':
            pygame.draw.polygon(self.image, 'gray', s,(s*0.5,0),(s,s),(0,s))
        if board[bleh][bluh][1]=='trees':
            pygame.draw.line(self.image,'brown',(s*0.5,s*0.5),(s*0.5,s),5)
            pygame.draw.rect(self.image,[0,100,0],(0,0,s,s*0.5))
        if board[bleh][bluh][1]=='sheep':
            pygame.draw.rect(self.image,'white',(s*0.25,0,s*3*0.25,s*0.5))
            pygame.draw.rect(self.image,'black',(0,0,s*0.25,s*0.25))
            pygame.draw.line(self.image,'black',(s*0.3,s*0.5),(s*0.3,s),3)
            pygame.draw.line(self.image,'black',(s*0.9,s*0.5),(s*0.9,s),3)


screen=pygame.display.set_mode((width, height))
board=[]
first=1
map=make_map((72,36), blur_size=3, max_value=1, integer=False)
toisland=map
map=islandify(toisland, 10, 2)
for bleh in range(72):
    board.append([])
    for bluh in range(36):
        dograss=4
        domountains=1
        dotrees=2
        dosheep=3
        dowater=2
        if map[bleh,bluh]>0 and map[bleh,bluh]<0.25:
            dograss=1
            domountains=1
            dotrees=1
            dosheep=1
            dowater=10
        elif map[bleh,bluh]>0.25 and map[bleh,bluh]<0.5:
            dograss=10
            domountains=1
            dotrees=1
            dosheep=1
            dowater=1
        elif map[bleh,bluh]>0.5 and map[bleh,bluh]<0.75:
            dograss=1
            domountains=1
            dotrees=10
            dosheep=1
            dowater=1
        elif map[bleh,bluh]>0.75 and map[bleh,bluh]<1:
            dograss=1
            domountains=10
            dotrees=1
            dosheep=1
            dowater=1
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
class team:
    def __init__(self,x,y,kind,board):
        self.x=x
        self.y=y
        self.kind=kind
        self.board=board
        self.gox=self.x
        self.goy=self.y
        self.life=100
    def tell(startx,starty,x,y,harvest):
        for bleh in range(len(self.board)):
            for bluh in range(len(self.board[bleh])):
                if bleh>startx and bleh<x and bluh>starty and bluh<y:
                    if self.kind=='miner' and self.board[bleh][bluh][1]=='mountains':
                        return bleh,bluh,None
                    if self.kind=='lumberjack' and self.board[bleh][bluh][1]=='trees':
                        return bleh,bluh,None
                    if self.kind=='farmer' and self.board[bleh][bluh][1]=='grass' and harvest==True:
                        return bleh,bluh,True
                    if self.kind=='farmer' and self.board[bleh][bluh][1]=='grass' and harvest==False:
                        return bleh,bluh,False
                    if self.kind=='waterbro' and self.board[bleh][bluh][1]=='water':
                        return bleh,bluh,None
                    if self.kind=='seller' and self.board[bleh][bluh][1]=='sheep':
                        return bleh,bluh,None
        def move():
            if self.gox>self.x:
                self.x+=1
            else:
                self.x-=1
            if self.goy>self.y:
                self.y+=1
            else:
                self.y-=1
        def draw():
            pygame.draw.line(screen,'red',((self.x*20)-50,self.y+50),(((self.x*20)-50)+self.life,self.y+50),3)
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
