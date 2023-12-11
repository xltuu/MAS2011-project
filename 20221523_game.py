import pygame
import random
import time
from os import path
import os
import sys

pygame.init()

# 변수들 설정

WIDTH = 840
HEIGHT = 650
FPS = 40

LANE_COUNT = 4  # Adjust as needed based on your game's design
lane_positions = [int(WIDTH / LANE_COUNT * i) for i in range(LANE_COUNT)]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

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
item_list=['star.svg', 'banana.png', 'present.png', 'bell.png']
for img in item_list:
    item_images.append(pygame.image.load(path.join(img_dir, img)).convert())

star_sound=pygame.mixer.Sound(path.join(snd_dir, 'twinkle.mp3'))
banana_sound=pygame.mixer.Sound(path.join(snd_dir, 'banana.wav'))
present_sound=pygame.mixer.Sound(path.join(snd_dir, 'tada.mp3'))
bell_sound=pygame.mixer.Sound(path.join(snd_dir, 'bell.flac'))
ending_sound=pygame.mixer.Sound(path.join(snd_dir, 'hohoho.mp3'))
pygame.mixer.music.load(path.join(snd_dir, 'JingleBells.mp3'))
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(loops=-1)

# txt 읽어서 가장 높은 점수 반환
def read_score():
    score_filename = "score.txt"  # You can adjust the filename as needed
    highest_score=0
    if os.path.exists(score_filename):
        with open(score_filename, "r") as file:
            scores = file.readlines()  # 모든 줄을 읽어 리스트로 저장
            for score in scores:
                try:
                    score_value = int(score.strip())  # 줄바꿈 문자 제거 후 정수로 변환
                    if score_value > highest_score:
                        highest_score = score_value
                except ValueError:
                    pass  # 숫자로 변환할 수 없는 경우 무시
    return highest_score

def write_score(score):
    score_filename = "score.txt"
    intscore=int(round(score,2))
    with open(score_filename, "a") as file:
        file.write(str(intscore)+"\n")

# Function to display the score on the screen
def display_score():
    global score_button_clicked

    font = pygame.font.Font('Giants-Inline.otf', 74)
    score = read_score()
    text = font.render(f"High Score: {score}", True, WHITE)
    screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.flip()
    pygame.time.wait(2000)  # 2 seconds delay
    score_button_clicked=False
    score_button.clicked=False

    main()  # Go back to the main menu after displaying the score


# 방해물 객체 2개 생성
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
                font = pygame.font.Font('Giants-Inline.otf', 74)
                text = font.render("Car Racing Game", True, WHITE)
                screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2 ))

                start_button.draw((196, 183, 255), "START")
                score_button.draw((255, 255, 0), "SCORE")

            if not start_button_clicked:
                if end_button.is_clicked():
                    pygame.mixer.music.stop()
                    ending_sound.play()
                    pygame.time.wait(5000)  # 5초 대기
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

    item_respawn_time = random.randint(1, 7)  # item이 제거된 후 재생성까지의 시간 (초)
    item_respawn_timer = 0

    game_exit = False
    game_over=False
    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        score += 0.1  # 예시로, 매 프레임마다 스코어를 1씩 증가시킵니다.

        #화면 속도
        screenv=player.keyclick()

        # 배경 화면 이동
        yb1 += screenv
        yb += screenv
        screen.blit(background, (xb, yb+100))
        screen.blit(background, (xb1, yb1+100))
        # 화면에 스코어 표시
        font = pygame.font.Font('Giants-Inline.otf', 36)  # 폰트와 크기 설정
        score_text = font.render(f"Score: {int(score)}", True, WHITE)  # 스코어 텍스트 렌더링
        score_rect = score_text.get_rect()
        score_rect.topright = (WIDTH - 10, 10)  # 화면 오른쪽 상단에 위치 설정
        screen.blit(score_text, score_rect)  # 스코어 화면에 그리기

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
                banana_sound.play()
                for objcar in objcars:
                    objcar.speedy-=1
            elif item_name == 'star':
                star_sound.play()
                if(player.shield>=100):
                    continue
                else:
                    player.shield += 10
                    if(player.shield>=100):
                        player.shield=100
            elif item_name=='present':
                present_sound.play()
                if(player.shield>=100):
                    continue
                else:
                    player.shield += 20
                    if(player.shield>=100):
                        player.shield=100
            elif item_name=='bell':
                bell_sound.play()
                score+=50

        if player.shield <=0:
            game_exit=True
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

#게임 종료된 후 화면
def overscreen():
    global score,game_over, start_button_clicked

    # 화면을 지우고 게임 오버 텍스트를 표시하는 등의 작업을 수행
    screen.fill(BLACK)
    font = pygame.font.Font('Giants-Inline.otf', 74)
    text = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Score: {int(score)}", True, WHITE)
    screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2-5))
    screen.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, HEIGHT / 2 - score_text.get_height() / 2+70))
    pygame.display.flip()

    write_score(score)

    # 잠시 대기한 뒤 프로그램 종료
    pygame.time.wait(2000)  # 2초 대기

    # 버튼 클릭, 점수 초기화
    player.shield=100
    game_over=True
    start_button_clicked=False
    start_button.clicked=False
    score=0

    #player, objcar 위치 초기화
    player.rect.centerx = WIDTH // 2  # 화면 가로 중앙
    player.rect.centery = HEIGHT // 2  # 화면 세로 중앙
    i=0
    for objcar in objcars:
        objcar.rect = objcar.image.get_rect()
        objcar.rect.x += 385*i + 187
        objcar.rect.y += 450
        i+=1

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

        self.rect.x=random.randint(50, WIDTH-60)

    def update(self):
        self.rect.y+=5
        if self.rect.y > HEIGHT:
            self.rect.y = -HEIGHT
            self.rect.x = random.randint(50, WIDTH-50)


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
    def __init__(self, x, y, w, h, r):
        self.rect = pygame.Rect(x, y, w, h)
        self.radius=r
        self.clicked = False  # Track the button state

    def draw(self, color, text):
        # 둥근 모서리 그리기
        pygame.draw.rect(screen, color, (self.rect.x + self.radius, self.rect.y, self.rect.width - 2*self.radius, self.rect.height))
        pygame.draw.rect(screen, color, (self.rect.x, self.rect.y + self.radius, self.rect.width, self.rect.height - 2*self.radius))
        pygame.draw.circle(screen, color, (self.rect.left + self.radius, self.rect.top + self.radius), self.radius)
        pygame.draw.circle(screen, color, (self.rect.right - self.radius, self.rect.top + self.radius), self.radius)
        pygame.draw.circle(screen, color, (self.rect.left + self.radius, self.rect.bottom - self.radius), self.radius)
        pygame.draw.circle(screen, color, (self.rect.right - self.radius, self.rect.bottom - self.radius), self.radius)
        font = pygame.font.Font('Giants-Inline.otf', 36)
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

        # 속도 감소 로직
        if self.speedx > 0:
            self.speedx -= 0.1  # 오른쪽으로 감속
        elif self.speedx < 0:
            self.speedx += 0.1  # 왼쪽으로 감속

        if self.speedy > 0:
            self.speedy -= 0.1  # 아래로 감속
        elif self.speedy < 0:
            self.speedy += 0.1  # 위로 감속

        # 속도 업데이트
        self.speedx += self.acceleration
        self.speedy += self.acceleration_y

        # 속도가 충분히 낮아지면 완전히 멈춤
        if abs(self.speedx) < 2:
            self.speedx = 0
            self.acceleration = 0  # 가속도도 0으로 설정

        if abs(self.speedy) < 2:
            self.speedy = 0
            self.acceleration_y = 0  # Y축 가속도도 0으로 설정


        for objcar in objcars:
            if pygame.sprite.collide_rect(self, objcar):
                self.shield-=1
                # Player가 objectCar의 왼쪽에 있는 경우
                if self.rect.right > objcar.rect.left and self.rect.centerx < objcar.rect.centerx:
                    self.rect.right = objcar.rect.left

                # Player가 objectCar의 오른쪽에 있는 경우
                elif self.rect.left < objcar.rect.right and self.rect.centerx > objcar.rect.centerx:
                    self.rect.left = objcar.rect.right

                # 반대 방향으로 속도 설정
                self.speedx = -self.speedx
                self.speedy = -self.speedy
                objcar.speedx = -objcar.speedx
                objcar.speedy = -objcar.speedy

                # 가속도 반전
                self.acceleration = -self.acceleration
                objcar.acceleration = -objcar.acceleration


        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # 화면 경계 처리
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
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

        self.speedx=random.randint(-10, 10)
        self.speedy=2
        self.acceleration=0

    def update(self):

        self.rect.x += self.speedx
        self.rect.y -= self.speedy
        
        # 화면 밖으로 나가지 않도록 제한
        if self.rect.right > WIDTH:
            self.speedx=-2
        if self.rect.left < 0:
            self.speedx+=2
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.speedy=2
        if self.rect.top < 0:
            self.rect.bottom = HEIGHT
            self.rect.x=random.randint(50, WIDTH-50)

        for other in objcars:
            if other != self and self.rect.colliderect(other.rect):
                # 충돌 시 반대 방향으로 속도 설정
                if self.rect.x < other.rect.x:  # self가 other보다 왼쪽에 있는 경우
                    self.rect.x -= 2  # self를 더 왼쪽으로 이동
                    other.rect.x += 2  # other를 오른쪽으로 이동
                else:  # self가 other보다 오른쪽에 있는 경우
                    self.rect.x += 2  # self를 오른쪽으로 이동
                    other.rect.x -= 2  # other를 왼쪽으로 이동

                self.speedx = -self.speedx
                self.speedy = -self.speedy
                other.speedx = -other.speedx
                other.speedy = -other.speedy


        if pygame.sprite.collide_rect(self, player):
                # self.shield-=1
                # Player가 objectCar의 왼쪽에 있는 경우
                if self.rect.right > player.rect.left and self.rect.centerx < player.rect.centerx:
                    self.rect.right = player.rect.left

                # Player가 objectCar의 오른쪽에 있는 경우
                elif self.rect.left < player.rect.right and self.rect.centerx > player.rect.centerx:
                    self.rect.left = player.rect.right

                # 반대 방향으로 속도 설정
                self.speedx = -self.speedx
                self.speedy = -self.speedy

                # 가속도 반전
                self.acceleration = -self.acceleration

        # 속도 감소 로직
        if self.speedx > 0:
            self.speedx -= 0.1  # 오른쪽으로 감속
        elif self.speedx < 0:
            self.speedx += 0.1  # 왼쪽으로 감속

        # 속도가 0에 도달하면 정지
        if abs(self.speedx) < 1:
            self.speedx = random.randint(-2, 2)
        if abs(self.speedy) < 1:
            self.speedy = 2

        if self.speedy > 0:
            self.speedy -= 0.1  # 아래로 감속
        elif self.speedy < 0:
            self.speedy += 0.1  # 위로 감속

        # 위치 업데이트
        self.rect.x += self.speedx
        self.rect.y -= self.speedy


    def draw(self, screen):
        self.image.set_colorkey(BLACK)
        screen.blit(self.image, self.rect)


start_button = Button(WIDTH/6, HEIGHT/5*4, 150, 50,12)  # 시작 버튼
score_button=Button(WIDTH//2-60, HEIGHT/5*4, 150, 50,12)    # 점수 버튼
end_button = Button(WIDTH/6*4+25, HEIGHT/5*4, 150, 50,12)  # 종료 버튼

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
