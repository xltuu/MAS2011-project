import pygame
import time
import sys
 
pygame.init()

# 색상
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
blue = (0,0,255)
orange = (255,165,0)

# 화면 크기
display_width = 800
display_height = 600


# 화면 설정 
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('카레이서')
carImg = pygame.image.load('car.png')
pygame.display.set_icon(carImg)
clock = pygame.time.Clock()

# 배경 화면
def background():    
    gameDisplay.blit(pygame.image.load("highway.png"), (100, 0))

# 배경 화면 1
def background1():    
    gameDisplay.blit(pygame.image.load("highway.png"), (100, 0))    

# 레이싱 카
def car(x,y):
    gameDisplay.blit(carImg,(x,y))    
 

# 텍스트 설정
def text_objects(text, font):
    textSurface = font.render(text, True, blue)
    return textSurface, textSurface.get_rect()
 
# 버튼
def button(txt,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
        
    smallText = pygame.font.SysFont("malgungothic",20)
    textSurf, textRect = text_objects(txt, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)
    
# 게임 종료
def quitgame():
    pygame.quit()
    sys.exit()


def introScreen():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               quitgame()
                
        gameDisplay.fill(white)
        background()
        largeText = pygame.font.SysFont("malgungothic",115)
        TextSurf, TextRect = text_objects("카레이서", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        button("시작",150,450,100,50,green,orange,gameScreen)
        button("종료",550,450,100,50,red,orange,quitgame)

        pygame.display.update()
        clock.tick(15)

def gameScreen():
   
    x = (display_width * 0.45)
    y = (display_height * 0.7)
 
    gameExit = False
 
    while not gameExit:
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
 
        gameDisplay.fill(white)
        background1()
 
        car(x,y)
        
        pygame.display.update()
        clock.tick(60)
        

introScreen()
