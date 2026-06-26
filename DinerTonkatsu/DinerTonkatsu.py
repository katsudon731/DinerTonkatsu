import pygame
import sys
import os

pygame.init()

# Window setup
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Закусочная Тонкацу")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
RED = (255, 0, 0)

# Fonts
FONT = pygame.font.Font(None, 36)

# Load images safely: if missing, game continues without them
def load_image(filename):
    try:
        img = pygame.image.load(filename).convert()
        return img
    except FileNotFoundError:
        print("Image not found: " + filename)
        return None

background = load_image("https://sun9-56.userapi.com/s/v1/ig2/FgSYR5hQRk86dbiqtJiix5_dLlLjUqGoi1ioEjqUTAC0gh47wG4UcoZa9AQJSAXSXN90z28fKsfPHTv2YsCIvALV.jpg?quality=95&as=32x24,48x36,72x54,108x81,160x120,240x180,360x270,480x360,540x405,640x480&from=bu&u=gbFwoWnMJTLaZSezDrwWZIlR2sPtJesnzbrs_8ummfs&cs=640x0")
chef_sprite = load_image("chef.png")

if background:
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# State variables (names in English as per coding standards)
dialogue_index = 0
state = "dialogue"      # "dialogue" or "choice"
player_choice = None
fear_level = 0          # 0-3

# Dialogues and choices (Russian text)
dialogues = [
    "Добро пожаловать в закусочную Тонкацу! Тут всё нормально... или нет?",
    "Вы замечаете странные вещи: меню меняется само по себе.",
    "Что будете делать?"
]

choices = [
    ["Поговорить с шефом", "Осмотреть кухню", "Покинуть закусочную"]
]

# Text rendering
def draw_text(text, x, y, color=WHITE):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        txt_surface = FONT.render(line, True, color)
        screen.blit(txt_surface, (x, y + i * 40))

# Main loop
running = True
while running:
    # Draw background or fill with color
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill(GRAY)

    # Draw chef sprite if available
    if chef_sprite:
        chef_x = WIDTH - chef_sprite.get_width() - 30
        chef_y = HEIGHT // 2 - chef_sprite.get_height() // 2
        screen.blit(chef_sprite, (chef_x, chef_y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if state == "dialogue":
                if dialogue_index < len(dialogues) - 1:
                    dialogue_index += 1
                else:
                    state = "choice"
            elif state == "choice":
                mouse_x, mouse_y = event.pos
                for i, choice in enumerate(choices[0]):
                    btn_rect = pygame.Rect(100, 500 + i * 60, 700, 50)
                    if btn_rect.collidepoint(mouse_x, mouse_y):
                        player_choice = i
                        if i == 0:
                            fear_level = max(0, fear_level - 1)
                        elif i == 1:
                            fear_level = min(3, fear_level + 1)
                        elif i == 2:
                            fear_level = 3
                        running = False

    # Draw dialogue or choices
    if state == "dialogue":
        draw_text(dialogues[dialogue_index], 50, 50)
    elif state == "choice":
        for i, ch in enumerate(choices[0]):
            rect = pygame.Rect(100, 500 + i * 60, 700, 50)
            pygame.draw.rect(screen, BLACK, rect)
            draw_text(ch, rect.x + 10, rect.y + 10)

    # Display fear level
    fear_status = ["Спокойствие", "Тревога", "Страх", "Паника"]
    draw_text("Степень страха: " + fear_status[fear_level], 50, 10, RED)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()

