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

peeps=[]
reset = False
exit = False

def speed_changed_callback(new_speed):
    for peep in peeps:
        peep.speed = (new_speed)/50
def reset_button_callback(new_reset):
    global reset
    reset = new_reset
    print('reset_callback')
def exit_button_callback(new_exit):
    global exit
    exit = new_exit
    print('exit_callback')

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

    board, tiles = create_board(width_in_tiles, height_in_tiles)

    first=1
    yx=randint(1,width_in_tiles)
    yy=randint(1,height_in_tiles)
    cool=0
    x,y=pygame.mouse.get_pos()
    test=Adjust(100,200,0.5,1440,720)

    for k in range(20):
        peeps.append(Entity(randint(1,144),randint(1,72),board))
    space=0
    label = Label(text="Menu")
    speed_slider = SliderControl(name="Speed", min=3, max=10, value=5,
                                value_change_callbacks=[speed_changed_callback])
    zoom_slider = IncrementControl(
                name="Zoom",
                min=1, max=100, value=10,
                value_change_callbacks=[change_tile_size]
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
    while True:
        # If necessary, update tile images for new zoom
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
        last=zoom_slider.get_value()
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
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if not paused:
                    if event.button == 1:
                        x_tile, y_tile = screen2Tile(x, y)
                        peeps.append(Entity(int(x_tile), int(y_tile), board))
            menu.handle_event(event)

        key=pygame.key.get_pressed()

        tiles.draw(screen)
        now=zoom_slider.get_value()
        if now!=last:
            if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT]:
                zoom_slider.set_value(10)

        if not paused:
            killed=[]
            for peep in peeps:
                peep.harvest()
                kill=peep.move()
                if kill!=False:
                    peep.life -= kill
                if peep.life==0:
                    killed.append(peep)
                peep.update()
            for peep in killed:
                peeps.remove(peep)

        if reset:
            break
        if exit:
            pygame.quit()
            sys.exit()

        for peep in peeps:
            peep.draw(screen)

        if paused:
            menu.update()
            menu.draw(screen)
            #Controls.menu('arial.ttf',[0,0,0],'menu',screen,('hi',0),('hi',1),('hi',2),('hi',3),('hi',4),('hi',5),('hi',6),('hi',7))
        pygame.draw.circle(screen,[255,100,100],(x,y),5)
        pygame.display.flip()
        Clock.tick(60)
