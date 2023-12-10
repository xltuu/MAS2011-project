import pygame
import random
import time
from os import path
import os
import sys

pygame.init()

WIDTH = 840
HEIGHT = 650
FPS = 40

LANE_COUNT = 4  # Adjust as needed based on your game's design
lane_positions = [int(WIDTH / LANE_COUNT * i) for i in range(LANE_COUNT)]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

img_dir = path.join(path.dirname(__file__), 'img')
start_button_clicked = False
score_button_clicked = False
game_over=True

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("20221523_권지수")
carImg = pygame.image.load('img/car.png')
pygame.display.set_icon(carImg)
clock = pygame.time.Clock()
score=0

background = pygame.image.load(path.join(img_dir, "highway.png")).convert()
background_rect = background.get_rect()

player_img = pygame.image.load(path.join(img_dir, "car.png")).convert()
objcar_images = []
objcar_list = ['objcar1.png', 'objcar2.png', 'objcar3.png', 'objcar4.png']
for img in objcar_list:
    objcar_images.append(pygame.image.load(path.join(img_dir, img)).convert())

item_images=[]
item_list=['star.svg', 'banana.png']
for img in item_list:
    item_images.append(pygame.image.load(path.join(img_dir, img)).convert())

# Function to read the score from the memo pad file
def read_score():
    score_filename = "score.txt"  # You can adjust the filename as needed
    if os.path.exists(score_filename):
        with open(score_filename, "r") as file:
            score = file.read()
            return int(score)
    return 0  # Return 0 if the file doesn't exist or there's an issue reading the score

def write_score(score):
    score_filename = "score.txt"
    with open(score_filename, "w") as file:
        file.write(str(score))

# Function to display the score on the screen
def display_score():
    global score_button_clicked

    font = pygame.font.Font(None, 74)
    score = read_score()
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.flip()
    pygame.time.wait(2000)  # 2 seconds delay
    score_button_clicked=False
    score_button.clicked=False

    main()  # Go back to the main menu after displaying the score


# 방해물 객체 4개 생성
def newobjcar(i):
    oc = objectCar(i)
    objcars.add(oc)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, (255, 85, 142), fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

# Main loop
def main():
    global start_button_clicked,score, score_button_clicked,game_over  # if you still need this global variable

    running = True
    game_over=True
    start_time=pygame.time.get_ticks()
    while running:
        if game_over: # 시작 화면 draw
            clock.tick(FPS)
            screen.fill(BLACK)
            screen.blit(background, background_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if start_button.is_clicked():
                start_button_clicked = True  # Update the global variable if needed
                gameScreen()
            elif score_button.is_clicked():
                score_button_clicked=True
                display_score()
            else: # 버튼이 아무것도 클릭되지 않았을 때
                # Display "Car Racing Game" in the center of the screen
                font = pygame.font.Font(None, 74)
                text = font.render("Car Racing Game", True, WHITE)
                screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))

                start_button.draw((196, 183, 255), "START")
                score_button.draw((255, 255, 0), "SCORE")

            if not start_button_clicked:
                if end_button.is_clicked():
                    running = False
                    sys.exit()
                else:
                    end_button.draw((255, 0, 0), "END")

            pygame.display.flip()
            clock.tick(FPS)
    pygame.quit()


# 시작 버튼 누른 뒤 화면
def gameScreen():
    global score,game_over
    # 화면 좌표
    xb, yb = 0, 0
    xb1 = 0
    yb1 = -background_rect.height

    item_respawn_time = 5  # item이 제거된 후 재생성까지의 시간 (초)
    item_respawn_timer = 0

    game_exit = False
    game_over=False
    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        #화면 속도
        screenv=player.keyclick()

        # 배경 화면 이동
        yb1 += screenv
        yb += screenv
        screen.blit(background, (xb, yb))
        screen.blit(background, (xb1, yb1))
        if yb > background_rect.height:
            yb = -background_rect.height

        if yb1 > background_rect.height:
            yb1 = -background_rect.height

        player.update()
        screen.blit(player.image, player.rect)
        draw_shield_bar(screen,5, 5, player.shield)

        item_hits = pygame.sprite.spritecollide(player, items, True)
        for item in item_hits:
            item_name = item.get_item_name()
            if item_name == 'banana':
                for objcar in objcars:
                    objcar.rect.y-=10
            elif item_name == 'star':
                if(player.shield>=100):
                    continue
                else:
                    player.shield += 10

        if player.shield <=0:
            game_exit=True
            elapsed_time=(pygame.time.get_ticks())//1000  # 경과 시간(초)
            score=elapsed_time*10
            # game_over=True
            overscreen()
            return

        # objcar 업데이트 및 그리기
        for objcar in objcars:
            objcar.update()
            objcar.draw(screen)

        # 아이템 업데이트 및 그리기
        items.update()
        items.draw(screen)
        
        pygame.display.update()
        clock.tick(60)

        # item 재생성 타이머 업데이트
        if not items:
            item_respawn_timer += 1

        # item 재생성
        if item_respawn_timer >= item_respawn_time * FPS:
            items.add(Item(random.choice(item_list)))
            item_respawn_timer = 0

def overscreen():
    global score,game_over, start_button_clicked
    # 화면을 지우고 게임 오버 텍스트를 표시하는 등의 작업을 수행
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    screen.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, HEIGHT / 2 - score_text.get_height() / 2+50))
    pygame.display.flip()

    write_score(score)

    # 잠시 대기한 뒤 프로그램 종료
    pygame.time.wait(2000)  # 2초 대기

    # 버튼 클릭 초기화
    player.shield=100
    game_over=True
    start_button_clicked=False
    start_button.clicked=False
    main()

# 아이템 클래스
class Item(pygame.sprite.Sprite):
    def __init__(self, image_filename):
        super(Item, self).__init__()
        self.image_orig = pygame.image.load(path.join(img_dir, image_filename)).convert()
        self.image_orig.set_colorkey(BLACK)
        self.image = pygame.transform.scale(self.image_orig.copy(), (85, 85))
        self.rect = self.image.get_rect()
        self.item_name = path.splitext(path.basename(image_filename))[0]

        # self.rect.centerx = WIDTH // 2  # 화면 가로 중앙

    def update(self):
        self.rect.y+=5
        if self.rect.y > HEIGHT:
            self.rect.y = -HEIGHT
            self.rect.x = WIDTH/2


    def draw(self, screen):
        x =random.randint(0, WIDTH)
        y = self.rect.y+600
        self.image.set_colorkey(BLACK)
        screen.blit(self.image, (x, y))
    
    def get_item_name(self):
        # 이미지 파일명에서 확장자를 제외한 부분을 반환
        return self.item_name

# 버튼 클래스
class Button():
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.clicked = False  # Track the button state

    def draw(self, color, text):
        pygame.draw.rect(screen, color, self.rect)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.rect.collidepoint(mouse_pos) and click[0] and not self.clicked:
            self.clicked = True  # Update the button state
        return self.clicked

# 플레이어 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.transform.scale(player_img, (80, 128))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2  # 화면 가로 중앙
        self.rect.centery = HEIGHT // 2  # 화면 세로 중앙

        self.speedy = 0  # 초기화 추가
        self.speedx = 0  # 초기화 추가
        
        self.upclick=False
        self.downclick=False

        self.mask = pygame.mask.from_surface(self.image)

        self.shield=100
        self.acceleration=0
        self.acceleration_y=0

    def update(self):
        # self.speedx = 0
        self.speedx += self.acceleration
        self.speedy += self.acceleration

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP]:
            self.speedy = -5
            self.upclick=True
        elif keystate[pygame.K_DOWN]:
            self.speedy = 5
            self.downclick=True
        elif keystate[pygame.K_LEFT]:
            self.speedx = -5
        elif keystate[pygame.K_RIGHT]:
            self.speedx = 5
        else:
            self.speedy = 0
        # self.rect.y += self.speedy
        # self.rect.x += self.speedx

         # 가속도의 부호를 속도의 방향에 따라 조정
        if self.speedx > 0:
            self.acceleration = -1  # 오른쪽으로 이동 시 감속
        elif self.speedx < 0:
            self.acceleration = 1   # 왼쪽으로 이동 시 감속

        # 속도 업데이트
        self.speedx += self.acceleration

        # 좌표 업데이트
        self.rect.x += self.speedx

        # 속도가 0에 가까워지면 멈추도록 설정
        if abs(self.speedx) < 2: self.speedx = 0

        # Y축에 대해서도 동일하게 적용
        if self.speedy > 0:
            self.acceleration_y = -1
        elif self.speedy < 0:
            self.acceleration_y = 1

        self.speedy += self.acceleration_y
        self.rect.y += self.speedy

        if abs(self.speedy) < 2: self.speedy = 0
            
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
        
    def keyclick(self):
        if self.upclick==True:
            return 13
        elif self.downclick==True:
            return -13
        return 5

# objcar 클래스
class objectCar(pygame.sprite.Sprite):
    def __init__(self, image_index):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = []
        for objcar_img in objcar_images:
            img = pygame.transform.scale(objcar_img, (80, 128))
            img.set_colorkey(BLACK)
            self.image_orig.append(img)

        self.image_index = image_index
        self.image = self.image_orig[image_index]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.x += 385*self.image_index + 187
        self.rect.y += 450

    def update(self):
        # objectCar가 player를 따라가도록 설정
        if player.speedy<0:
            self.rect.x+=random.randint(-10, 10)
            self.rect.y+=player.speedy*1.5
        else:
            self.rect.y-=player.speedy

        # 화면 밖으로 나가지 않도록 제한
        # if self.rect.right > WIDTH:
        #     self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = HEIGHT

        #player와 충돌 검사
        if pygame.sprite.collide_mask(self,player):
            player.shield-=20
            self.bounce_effect()

    def bounce_effect(self):
        player.speedx = 10 if self.rect.centerx < player.rect.centerx else -10
        player.speedy = 10 if self.rect.centery < player.rect.centery else -10

        self.speedx = -player.speedx
        self.speedy = -player.speedy

        # 가속도 (또는 감속도) 설정
        player.acceleration = 0.1  # 예시 값, 실제 게임에 맞게 조정 필요
        self.acceleration = -0.1  # 예시 값


    def draw(self, screen):
        self.image.set_colorkey(BLACK)
        screen.blit(self.image, self.rect)


start_button = Button(WIDTH/6, HEIGHT/5*4, 120, 50)  # 시작 버튼
score_button=Button(WIDTH//2-60, HEIGHT/5*4, 120, 50)    # 점수 버튼
end_button = Button(WIDTH/6*4+25, HEIGHT/5*4, 120, 50)  # 종료 버튼

all_sprites = pygame.sprite.Group()
objcars = pygame.sprite.Group()
player = Player()
items=pygame.sprite.Group()
# items.add(Item())
items.add(Item(random.choice(item_list)))
all_sprites.add(player)
# objcar=objectCar()
for i in range(2):
    newobjcar(i)

if __name__ == "__main__":
    main() 