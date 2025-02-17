import pygame
import sys
from PygameWidgets import *
from GenesisUtils import *
from random import randint, choice
from copy import copy
pygame.init()
Clock=pygame.time.Clock()

my_font = pygame.font.SysFont('Comic Sans MS', 50)
width=1440
height=720
screen=pygame.display.set_mode((width, height))

peeps=pygame.sprite.Group()
reset = False
exit = False

path_start = None
path_end = None

def speed_changed_callback(new_speed):
    for peep in peeps.sprites():
        peep.speed = (new_speed)/50
def reset_button_callback(new_reset):
    global reset
    reset = new_reset
def exit_button_callback(new_exit):
    global exit
    exit = new_exit
def zoom_changed_callback(new_tile_size):
    Tile.size = new_tile_size

while True:
    reset = False
    exit = False
    # Display loading screen
    screen.fill('blue')
    for event in pygame.event.get():
        pass
    text_surface=my_font.render('loading...', False, (255, 255, 255))
    screen.blit(text_surface, (470,335))
    pygame.display.flip()

    Clock=pygame.time.Clock()

    width_in_tiles = 72*2
    height_in_tiles = 36*2

    board = create_board(width_in_tiles, height_in_tiles)

    first=1
    yx=randint(1,width_in_tiles)
    yy=randint(1,height_in_tiles)
    cool=0
    x,y=pygame.mouse.get_pos()
    test=Adjust(100,200,0.5,1440,720)

    for k in range(20):
        peeps.add(Traveler(randint(0,143),randint(0,71),board))
    space=0
    label = Label(text="Menu")
    speed_slider = SliderControl(name="Speed", min=3, max=10, value=5,
                                value_change_callbacks=[speed_changed_callback])
    zoom_slider = IncrementControl(
                name="Zoom",
                min=1, max=100, value=10,
                value_change_callbacks=[zoom_changed_callback]
                )
    menu = ControlMenu(position=(width / 2, height / 2), anchor='C', column_alignment='center')
    reset_button = ButtonControl(name="Reset", value_change_callbacks=[reset_button_callback])
    exit_button = ButtonControl(name="Exit", value_change_callbacks=[exit_button_callback])
    do='''The population is
           {x}'''
    population = Label(text=do.format(x=str(len(peeps))))
    menu.add(label)
    menu.add(speed_slider)
    menu.add(zoom_slider)
    menu.add(reset_button)
    menu.add(population)
    menu.add(exit_button)
    #test=Adjust(720,360,0.5,100,300,start=0,color='white')
    old_tile_size = Tile.size

    paused = False
    pygame.mouse.set_visible(False)
    grab_start = None
    start_zone=None
    end_zone=None
    while True:
        # If necessary, update tile images for new zoom
        new_tile_size = Tile.size
        if new_tile_size != old_tile_size:
            board.update_image()
            board.update_rect()
            for peep in peeps.sprites():
                peep.update_image()
                peep.update_rect()
        old_tile_size = new_tile_size

        keys = pygame.key.get_pressed()

        ##try:
        ##    dude.makepath()
        ##    dude.move()
        ##except NameError:
        ##    pass
        x,y=pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    paused = not paused
                    population.set_text(do.format(x=str(len(peeps))))
            elif event.type==pygame.MOUSEWHEEL:
                old_x_tile, old_y_tile = screen2Tile(x, y)
                Tile.size += event.y
                new_x_screen, new_y_screen = tile2Screen(old_x_tile, old_y_tile)
                Tile.x0 += (new_x_screen - x)
                Tile.y0 += (new_y_screen - y)
            if event.type==pygame.MOUSEBUTTONDOWN:
                start_zone=list(screen2Tile(x,y))
                end_zone=list(screen2Tile(x,y))
            if event.type==pygame.MOUSEBUTTONUP:
                for peep in peeps:
                    zone(peep,start_zone,end_zone)
                start_zone=None
                end_zone=None
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if keys[pygame.K_LSHIFT]:
                    x_tile, y_tile = screen2Tile(x, y)
                    point = board[int(x_tile), int(y_tile)]
                    for peep in peeps.sprites():
                        peep.make_plan(point)
                elif keys[pygame.K_LCTRL]:
                    if event.button == 1:
                        x_tile, y_tile = screen2Tile(x, y)
                        peeps.add(Traveler(int(x_tile), int(y_tile), board))
                else:
                    if event.button == 1:
                        x_tile, y_tile = screen2Tile(x, y)


            menu.handle_event(event)

        if not paused:
            killed=[]
            for peep in peeps.sprites():
                peep.harvest()
                kill=peep.move()
                if kill!=False:
                    peep.life -= kill
                if peep.life==0:
                    killed.append(peep)

            peeps.update()
            for peep in killed:
                peeps.remove(peep)

        if reset:
            break
        if exit:
            pygame.quit()
            sys.exit()
        screen.fill('blue')
        board.draw(screen)
        peeps.draw(screen)
        if start_zone!=None:
            end_zone=list(screen2Tile(x,y))
        if start_zone!=None and (abs(start_zone[0]-end_zone[0])>4 or abs(start_zone[1]-end_zone[1])>4):
            ul_zone=tile2Screen(min(start_zone[0], end_zone[0]), min(start_zone[1], end_zone[1]))
            lr_zone=tile2Screen(max(start_zone[0], end_zone[0]), max(start_zone[1], end_zone[1]))
            pygame.draw.rect(screen,'purple',(*ul_zone,lr_zone[0]-ul_zone[0], lr_zone[1]-ul_zone[1]),3)
        if paused:
            menu.update()
            menu.draw(screen)
            #Controls.menu('arial.ttf',[0,0,0],'menu',screen,('hi',0),('hi',1),('hi',2),('hi',3),('hi',4),('hi',5),('hi',6),('hi',7))
        pygame.draw.circle(screen,[255,100,100],(x,y),5)
        pygame.display.flip()
        Clock.tick(60)
        # breakpoint()
