import pygame
from random import randint
import sys
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
for bleh in range(72):
    board.append([])
    for bluh in range(36):
        board[bleh].append((randint(150,230),goodrand('choice',('grass',4),('mountains',1),('trees',2),('sheep',1),('water',2))))
yx=randint(1,72)
yy=randint(1,36)
cool=0
while True:
    screen.fill('blue')
    pygame.mouse.set_visible(False)
    x,y=pygame.mouse.get_pos()
    for event in pygame.event.get():
        pass
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
    pygame.display.flip()
    Clock.tick(60)
