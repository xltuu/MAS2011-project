import pygame
import sys

pygame.init()

# 화면 크기 및 색상 정의
screen_width, screen_height = 800, 600
background_color = (255, 255, 255)

# 화면 생성
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Button Name Change Example")

# 버튼 관련 변수
button_width, button_height = 200, 50
button_color = (0, 128, 255)
button_x, button_y = (screen_width - button_width) // 2, (screen_height - button_height) // 2

# 현재 버튼 이름을 나타내는 변수
button_name = "Button 1"

# 메인 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 마우스 클릭 시, 버튼 영역을 확인하여 버튼 이름 변경
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                if button_name == "Button 1":
                    button_name = "Button 2"
                else:
                    button_name = "Button 1"

    # 화면 그리기
    screen.fill(background_color)

    # 버튼 그리기
    pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))

    # 버튼 텍스트 추가
    font = pygame.font.Font(None, 36)
    text = font.render(button_name, True, (255, 255, 255))
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(text, text_rect)

    # 화면 업데이트
    pygame.display.flip()

# Pygame 종료
pygame.quit()
sys.exit()
