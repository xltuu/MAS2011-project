import pygame
import time
import sys
import random
 
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
objectImg = pygame.image.load('object1.png')
pygame.display.set_icon(carImg)
clock = pygame.time.Clock()
back = pygame.image.load("highway1.jpg")

background_size = back.get_size()
background_rect = back.get_rect()
w,h = background_size


# 카 넓이
car_width = 75

# 배경 화면
def background():    
    gameDisplay.blit(pygame.image.load("highway.jpg"), (100, 0))


# 플레이어
def car(x,y):
    gameDisplay.blit(carImg,(x,y))

# 오브젝트
def objects(objectx, objecty, objectw, objecth, color):
    pygame.draw.rect(gameDisplay, color, [objectx, objecty, objectw, objecth])
   
    

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

# 인트로 화면
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

# 게임 화면
def gameScreen():
    # 배경 좌표
    xb = 0
    yb = 0
    xb1 = 0
    yb1 = -h

    # 플레이어 좌표
    x = (display_width * 0.45)
    y = (display_height * 0.7)

    x_change = 0
    
    # 오브젝트 설정
    object_startx = random.randrange(0, display_width)
    object_starty = -600
    object_speed = 4
    object_width = 82
    object_height = 155
 
 
    gameExit = False
 
    while not gameExit:
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5

                    

                    
        x += x_change
        gameDisplay.fill(white)
        
        # 배경 화면 이동
        yb1 += 5
        yb += 5
        gameDisplay.blit(back,(xb+100,yb))
        gameDisplay.blit(back,(xb+100,yb1))
        if yb > h:
            yb = -h
          
        if yb1 > h:
            yb1 = -h             

                    
       
        # 오브젝트 생성
        objects(object_startx, object_starty, object_width, object_height, blue)
        object_starty += object_speed
 
        car(x,y)

        # 오브젝트 재생성
        if object_starty > display_height:
            object_starty = 0 - object_height
            object_startx = random.randrange(0,display_width-200)
            object_speed += 1
            if object_speed > 20:
                object_speed = 4
            
        # 이동 제한
        if x > display_width - car_width or x < 0:
            x_change = 0
        
        pygame.display.update()
        clock.tick(60)
        

introScreen()
