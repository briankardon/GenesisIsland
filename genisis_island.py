import pygame
from random import randint
import sys
from MapTools import *
from random import randint, choice
import numpy as np
from PygameWidgets import *
pygame.init()
Clock=pygame.time.Clock()
import time
while True:
    my_font = pygame.font.SysFont('Comic Sans MS', 50)
    width=1440
    height=720
    screen=pygame.display.set_mode((width, height))
    screen.fill('blue')
    for event in pygame.event.get():
        pass
    text_surface=my_font.render('loading...', False, (255, 255, 255))
    screen.blit(text_surface, (470,335))
    pygame.display.flip()
    Clock=pygame.time.Clock()
    def goodrand(which,*args):
        ret=[]
        for bleh in range(len(args)):
            for blah in range(args[bleh][1]):
                ret.append(str(args[bleh][0]))
        do=choice(ret)
        if which=='randint':
            return int(do)
        elif which=='choice':
            return do
    ###class building:
    ###    def __init__
    class Adjust:
        def __init__(self,x,y,node,width,height,start=0,color='white'):
            self.x=x
            self.y=y
            self.num=start
            self.node=node
            self.image=pygame.display.set_mode((width, height))
            self.image.fill('black')
            pygame.draw.lines(self.image, color, False, ((0,(self.image.height/3)),(self.image.width/2,0),(self.image.width,(self.image.height/3))), width=2)
            pygame.draw.lines(self.image, color, False, ((0,(self.image.height/3)),(self.image.width/2,self.image.height),(self.image.width,(self.image.height/3)*2)), width=2)
        def draw(self,surface):
            my_font = pygame.font.SysFont('Comic Sans MS', int(np.round(self.image.height/3)))
            text_surface=my_font.render(str(self.num), False, (255, 255, 255))
            self.image.blit(text_surface, (0,round(self.image.height/3)))
            surface.blit(self.image, (self.x,self.y))
        def updatenum(self):
            x,y=pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if abs(x-self.x)<(self.image.width/2) and (self.y-y)<0 and (self.y-y)>(-(self.image.height/3)):
                        self.num-=1
                        my_font = pygame.font.SysFont('Comic Sans MS', round(self.image.height/3))
                        text_surface=my_font.render(str(self.num), False, (255, 255, 255))
                    if abs(x-self.x)<(self.image.width/2) and (self.y-y)>0 and (self.y-y)<(-(self.image.height/3)):
                        self.num+=1
                        my_font = pygame.font.SysFont('Comic Sans MS', round(self.image.height/3))
                        text_surface=my_font.render(str(self.num), False, (255, 255, 255))
    class Entity:
        def __init__(self,x,y,board):
            self.x=x
            self.resources=[]
            self.y=y
            self.speed=1
            self.life=100
            self.first=1
            self.board=board
            self.cooldown=0
            self.gox=self.x-int(choice(['20','-20']))
            self.goy=self.y-int(choice(['20','-20']))
            self.moving=True
        def move(self):
            kill=False
            if self.cooldown==2:
                self.cooldown=0
                kill=25
                choicegox=['20','0','-20']
                choicegoy=['20','0','-20']
                for k in range(2):
                    move=randint(0,(len(choicegox)-1))
                    movey=randint(0,(len(choicegoy)-1))
                    if choicegoy==['20','-20']:
                        move=1
                    if move==0 or move==2:
                        movey=1
                    self.gox=self.x-int(choicegox[move])
                    self.goy=self.y-int(choicegoy[movey])
                    choicegox.pop(move)
                    choicegoy.pop(movey)
                    if self.first==0:
                        if self.gox==int(self.gox) and self.goy==int(self.goy) and self.gox==abs(self.gox) and (self.gox/10)<len(self.board) and self.goy==abs(self.goy) and (self.goy/10)<len(self.board[0]) and board[round(self.gox/10)][round(self.goy/10)].biome!='water':
                            if self.board[round(self.x/10)][round(self.y/10)].biome!='water':
                                kill=False
                                break
                self.moving=True
            if first==0:
                if self.board[round(self.x/10)][round(self.y/10)].biome=='trees':
                    pass
                    ##moveability=-((self.speed/4)/3)
                elif self.board[round(self.x/10)][round(self.y/10)].biome=='mounains':
                    pass
                    ##moveability=-(self.speed/2)
                else:
                    pass
            moveability=0
            self.first=0
            if self.x<self.gox:
                self.x+=self.speed+moveability
            elif self.x>self.gox:
                self.x-=self.speed+moveability
            if self.y<self.goy:
                self.y+=self.speed+moveability
            elif self.y>self.goy:
                self.y-=self.speed+moveability
            if self.x==self.gox and self.y==self.goy:
                self.moving=False
                self.cooldown=1
            if self.cooldown>0:
                self.cooldown+=1
            return kill
        def draw(self,surface):
            pygame.draw.circle(surface,'black',(self.x,self.y),5)
            pygame.draw.line(surface,'red',(self.x-12.5,self.y+10),((self.x-12.5)+(self.life/4),self.y+10),2)
        def harvest(self,tile='sheep'):
            try:
                if self.board[round(self.x/10)][round(self.y/10)].biome==tile:
                    for bleh in range(len(self.board[round(self.x/10)][round(self.y/10)].resources)):
                        self.resources.append(self.board.resources[bleh])
                        self.board.resources=[]
            except IndexError:
                pass
            return self.board
        def update_land(self,board):
            self.board=board
    class Controls:
        def menu(font,backgroundcolor,title,screen,*options):
            screen.fill(backgroundcolor)
            my_font = pygame.font.SysFont(font, 50)
            text_surface=my_font.render(str(title), False, (255, 255, 255))
            spacing=((screen.height-60)/len(options))
            my_font = pygame.font.SysFont(font, int(np.round(spacing-3)))
            hw=(screen.width)/2
            screen.blit(text_surface, (hw,50))
            x,y=pygame.mouse.get_pos()
            for bleh in range(len(options)):
                text_surface=my_font.render(options[bleh][0], False, (255, 255, 255))
                screen.blit(text_surface, (hw-(((spacing-3))/2),60+(bleh*spacing)))
                if y>60+(bleh*spacing) and y<60+(((bleh)+1)*spacing) and x>hw-(((spacing-3))/2) and x<hw+((spacing-3))/2:
                    return options[bleh][1]
            return None
    class Tile(pygame.sprite.Sprite):
        size=10
        def __init__(self, *args, tile_coords=(0, 0), resources=[],biome='plains', grass_color=None, **kwargs):
            super().__init__(*args, **kwargs)
            self.biome = biome
            self.entities = []
            self.resources = resources
            self.image = None
            if grass_color is None:
                self.grass_color=randint(150,230)
            else:
                self.grass_color = grass_color
            self.tile_coords = tile_coords
            self.update_image()
            self.update_rect()

        def update_rect(self):
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
                pygame.draw.polygon(self.image, 'gray', ((0, s), (s*0.5,0),(s,s),(0,s)))
            if self.biome == 'trees':
                pygame.draw.line(self.image,'brown',(s*0.5,s*0.5),(s*0.5,s),5)
                pygame.draw.rect(self.image,[0,100,0],(0,0,s,s*0.5))
            if self.biome == 'sheep':
                pygame.draw.rect(self.image,'white',(s*0.25,0,s*3*0.25,s*0.5))
                pygame.draw.rect(self.image,'black',(0,0,s*0.25,s*0.25))
                pygame.draw.line(self.image,'black',(s*0.3,s*0.5),(s*0.3,s),3)
                pygame.draw.line(self.image,'black',(s*0.9,s*0.5),(s*0.9,s),3)

    width_in_tiles = 72*2
    height_in_tiles = 36*2
    width=width_in_tiles * Tile.size
    height=height_in_tiles * Tile.size

    board = []
    tiles = pygame.sprite.Group()
    first=1
    map=make_map((width_in_tiles,height_in_tiles), blur_size=3, max_value=1, integer=False)
    map=islandify(map, 0.25, 5, min_value=-0.25, max_value=1)
    num_rivers = goodrand('randint', (7, 1), (8, 2), (9, 3), (10, 2), (11, 1))
    min_river_length = 10
    max_river_length = 100
    mid_river_length = (min_river_length + max_river_length)//2
    river_lengths = np.array(range(min_river_length, max_river_length))
    river_length_probs = (min_river_length + 1 - (((river_lengths-mid_river_length)**2)*min_river_length/(max_river_length-mid_river_length)**2)).astype('int')
    for r in range(30):
        length = goodrand('randint', *zip(river_lengths, river_length_probs))
        map = riverify(map, length=100)
    for bleh in range(width_in_tiles):
        board.append([])
        for bluh in range(height_in_tiles):
            dograss=1
            domountains=1
            dotrees=1
            dosheep=1
            dowater=1
            if map[bleh,bluh]<0.25:
                dowater=60
            elif map[bleh,bluh]>0.25 and map[bleh,bluh]<0.5:
                dograss=40
            elif map[bleh,bluh]>0.5 and map[bleh,bluh]<0.65:
                dotrees=40
            elif map[bleh,bluh]>0.65 and map[bleh,bluh]<1:
                domountains=40
            biome = goodrand('choice',('grass',dograss),('mountains',domountains),('trees',dotrees),('sheep',dosheep),('water',dowater))
            new_tile = Tile(tile_coords=(bleh, bluh), biome=biome)
            board[bleh].append(new_tile)
            tiles.add(new_tile)
    for bleh in range(len(board)):
        for bluh in range(len(board[bleh])):
            if board[bleh][bluh].biome=='sheep':
                board[bleh][bluh].resources=['meat','meat']
    yx=randint(1,width_in_tiles)
    yy=randint(1,height_in_tiles)
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
    class Team:
        def __init__(self,x,y,kind,board):
            self.x=x
            self.y=y
            self.kind=kind
            self.board=board
            self.gox=self.x
            self.goy=self.y
            self.life=10
            if kind=='miner':
                self.color='black'
            if kind=='miner':
                self.color='green'
            if kind=='miner':
                self.color='orange'
            if kind=='miner':
                self.color='blue'
            if kind=='miner':
                self.color='red'
        def tell(self,startx,starty,x,y,harvest):
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
        def move(self):
            if self.gox>self.x:
                self.x+=1
            else:
                self.x-=1
            if self.goy>self.y:
                self.y+=1
            else:
                self.y-=1
        def draw(self):
            x = self.x * Tile.size
            y = self.y * Tile.size
            pygame.draw.line(screen,'red',(x-50,y+50),((x-50)+self.life,y+50),3)
            pygame.draw.circle(screen,self.color,(x,y),10)
    x,y=pygame.mouse.get_pos()
    dude=Team(2,2,'miner',board)
    test=Adjust(100,200,0.5,1440,720)
    peeps=[Entity((randint(1,72))*20,(randint(1,36))*20,board),Entity(randint(1,1440),randint(1,720),board),Entity(randint(1,1440),randint(1,720),board),Entity(randint(1,1440),randint(1,720),board),Entity(randint(1,1440),randint(1,720),board),Entity(randint(1,1440),randint(1,720),board),Entity(randint(1,1440),randint(1,720),board),Entity(randint(1,1440),randint(1,720),board),Entity(randint(1,1440),randint(1,720),board),Entity(randint(1,1440),randint(1,720),board),Entity(randint(1,1440),randint(1,720),board),Entity(randint(1,1440),randint(1,720),board),Entity(randint(1,1440),randint(1,720),board),Entity(randint(1,1440),randint(1,720),board),Entity(randint(1,1440),randint(1,720),board),Entity(randint(1,1440),randint(1,720),board),Entity(randint(1,1440),randint(1,720),board),Entity(randint(1,1440),randint(1,720),board),Entity(randint(1,1440),randint(1,720),board),Entity(randint(1,1440),randint(1,720),board),Entity(randint(1,1440),randint(1,720),board),Entity(randint(1,1440),randint(1,720),board)]
    space=0
    label = Label(text="Menu")
    slider = SliderControl(name="Speed", min=3, max=10, value=5)
    menu = ControlMenu(position=(width / 2, height / 2), anchor='C', column_alignment='center')
    button = ButtonControl(name="Reset")
    exit = ButtonControl(name="Exit")
    do='''The population is
           {x}'''
    population = Label(text=do.format(x=str(len(peeps))))
    menu.add(label)
    menu.add(slider)
    menu.add(button)
    menu.add(population)
    menu.add(exit)
    #test=Adjust(720,360,0.5,100,300,start=0,color='white')
    while True:
        ##try:
        ##    dude.makepath()
        ##    dude.move()
        ##except NameError:
        ##    pass
        screen.fill('blue')
        pygame.mouse.set_visible(False)
        x,y=pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE and space==1:
                    space=0
                elif event.key==pygame.K_SPACE and space==0:
                    space=1
            if event.type==pygame.MOUSEBUTTONDOWN:
                if space==0:
                    peeps.append(Entity(x,y,board))
                ##dude=Pathfinder(board,x,y,yx,yy)
            menu.handle_event(event)
        key=pygame.key.get_pressed()
        tiles.draw(screen)
        ##pygame.draw.circle(screen,'red',(yx*20-10,yy*20-10),10)
        ##pygame.draw.line(screen,'white',(yx*20-10,yy*20-10),(x,y),2)
        ##try:
        ##    pygame.draw.circle(screen,'red',(dude.x*20,dude.y*20),10)
        ##except NameError:
        ##    pass
        #dude.draw()
        #test.draw(screen)
        #test.updatenum()
        #test.draw(screen)
        pop=[]
        for bleh in range(len(peeps)):
            if space==0:
                peeps[bleh].harvest()
                kill=peeps[bleh].move()
                if kill!=False:
                    peeps[bleh].life-=kill
                if peeps[bleh].life==0:
                    pop.append(bleh)
            peeps[bleh].draw(screen)
            if space==1:
                peeps[bleh].speed=round((round(slider.get_value()/2)*2)/5)
        for bleh in range(len(pop)):
            try:
                peeps.pop(pop[bleh])
            except IndexError:
                pass
        if button.get_value():
            if space==1:
                break
        if exit.get_value():
            if space==1:
                pygame.quit()
                sys.exit()
        population.set_text(do.format(x=str(len(peeps))))
        if space==1:
            menu.update()
            menu.draw(screen)
            #Controls.menu('arial.ttf',[0,0,0],'menu',screen,('hi',0),('hi',1),('hi',2),('hi',3),('hi',4),('hi',5),('hi',6),('hi',7))
        pygame.draw.circle(screen,[255,100,100],(x,y),5)
        pygame.display.flip()
        Clock.tick(60)
