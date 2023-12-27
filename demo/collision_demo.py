import pygame
import sys
import random

# 초기화
pygame.init()

# 화면 크기 및 설정
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sprite Collision")

# 색깔 정의
white = (255, 255, 255)

# 플레이어 클래스 정의
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height - 50)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < width:
            self.rect.x += self.speed

# 아이템 클래스 정의
class Item(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed = random.randrange(1, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > height:
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed = random.randrange(1, 5)

# 스프라이트 그룹 생성
all_sprites = pygame.sprite.Group()
items = pygame.sprite.Group()

# 플레이어 및 아이템 생성
player = Player()
all_sprites.add(player)

for _ in range(10):
    item = Item()
    all_sprites.add(item)
    items.add(item)

# 게임 루프
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 충돌 검사
    hits = pygame.sprite.spritecollide(player, items, True)
    for hit in hits:
        item = Item()
        all_sprites.add(item)
        items.add(item)

    # 업데이트
    all_sprites.update()

    # 화면 그리기
    screen.fill(white)
    all_sprites.draw(screen)

    # 화면 업데이트
    pygame.display.flip()

    # 초당 프레임 수 제한
    clock.tick(60)

pygame.quit()
sys.exit()
