import pygame
from MapTools import *
from random import randint, choice
import numpy as np

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

def is_legal_move(board,x,y,node='tile',tile_side=10):
    try:
        if node=='tile':
            if board[x-1][y-1].biome=='water':
                return False
            else:
                return True
        else:
            if board[(x)/tile_side][(y)/tile_side].biome=='water':
                return False
            else:
                return True
    except IndexError:
        return False

###class building:
###    def __init__
class Entity:
    def __init__(self,x,y,board):
        self.x=x
        self.resources=[]
        self.y=y
        self.speed=0.05
        self.life=100
        self.board=board
        self.cooldown=1
        self.gox=self.x
        self.goy=self.y
        self.moving=False
    def move(self):
        kill=False
        if not self.moving:
            # Not currently moving, pick a destination
            choicegox=[1, 0, -1]
            choicegoy=[1, 0, -1]
            movex=choice(choicegox)
            movey=choice(choicegoy)
            new_x = self.x + movex
            new_y = self.y + movey
            if is_legal_move(self.board, new_x, new_y):
                self.gox = new_x
                self.goy = new_y
                kill=False
                self.moving = True
        return kill

    def update(self):
        if self.x < self.gox:
            self.x += self.speed
        elif self.x > self.gox:
            self.x -= self.speed
        if self.y < self.goy:
            self.y += self.speed
        elif self.y > self.goy:
            self.y -= self.speed
        if abs(self.x - self.gox) < self.speed and abs(self.y - self.goy) < self.speed:
            # Made it to destination
            self.x = self.gox
            self.y = self.goy
            self.moving = False

    def draw(self,surface):
        pygame.draw.circle(surface,'black',((self.x * Tile.size),(self.y * Tile.size)), Tile.size/2)
        health_x0 = self.x * Tile.size - 12.5
        health_y0 = self.y * Tile.size + 10
        health_x1 = health_x0 + self.life/4
        health_y1 = self.y*Tile.size + 10
        pygame.draw.line(surface,'red',(health_x0, health_y0),(health_x1,health_y1),2)
    def harvest(self,tile='sheep'):
        try:
            if self.board[round(self.x/10)][round(self.y/10)].biome==tile:
                for bleh in range(len(self.board[round(self.x/10)][round(self.y/10)].resources)):
                    ####self.resources.append(self.board.resources[bleh])
                    ####self.board.resources=[]
                    pass
        except IndexError:
            pass
        return self.board
    def update_land(self,board):
        self.board=board

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

def change_tile_size(size):
    Tile.size = size

def create_board(width_in_tiles, height_in_tiles):
    width=width_in_tiles * Tile.size
    height=height_in_tiles * Tile.size

    board = []
    tiles = pygame.sprite.Group()
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
    return board, tiles

class Tile(pygame.sprite.Sprite):
    size=10
    def __init__(
            self,
            *args,
            tile_coords=(0, 0),
            height=0,
            resources=[],
            biome='plains',
            grass_color=None,
            **kwargs):
        super().__init__(*args, **kwargs)
        self.biome = biome
        self.entities = []
        self.resources = resources
        self.image = None
        self.height = height
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
