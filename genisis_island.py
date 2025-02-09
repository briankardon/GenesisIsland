import pygame
import sys
from PygameWidgets import *
from GenesisUtils import *
from random import randint, choice

pygame.init()
Clock=pygame.time.Clock()
my_font = pygame.font.SysFont('Comic Sans MS', 50)
width=1440
height=720
screen=pygame.display.set_mode((width, height))

while True:
    # Display loading screen
    screen.fill('blue')
    for event in pygame.event.get():
        pass
    text_surface=my_font.render('loading...', False, (255, 255, 255))
    screen.blit(text_surface, (470,335))
    pygame.display.flip()

    Clock=pygame.time.Clock()
    ###class building:
    ###    def __init__
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

    width_in_tiles = 72*2
    height_in_tiles = 36*2

    board, tiles = create_board(width_in_tiles, height_in_tiles)

    first=1
    yx=randint(1,width_in_tiles)
    yy=randint(1,height_in_tiles)
    cool=0
    x,y=pygame.mouse.get_pos()
    test=Adjust(100,200,0.5,1440,720)
    peeps=[Entity((randint(1,72))*20,(randint(1,36))*20,board)]
    for k in range(20):
        peeps.append(Entity(randint(1,1440),randint(1,720),board))
    space=0
    label = Label(text="Menu")
    slider = SliderControl(name="Speed", min=3, max=10, value=5)
    zoom_slider = SliderControl(
                name="Zoom",
                min=1, max=100, value=10,
                value_change_callbacks=[change_tile_size]
                )
    menu = ControlMenu(position=(width / 2, height / 2), anchor='C', column_alignment='center')
    button = ButtonControl(name="Reset")
    exit = ButtonControl(name="Exit")
    do='''The population is
           {x}'''
    population = Label(text=do.format(x=str(len(peeps))))
    menu.add(label)
    menu.add(slider)
    menu.add(zoom_slider)
    menu.add(button)
    menu.add(population)
    menu.add(exit)
    #test=Adjust(720,360,0.5,100,300,start=0,color='white')
    old_tile_size = Tile.size
    while True:
        new_tile_size = Tile.size
        if new_tile_size != old_tile_size:
            for tile in tiles.sprites():
                tile.update_image()
                tile.update_rect()
        old_tile_size = new_tile_size

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
