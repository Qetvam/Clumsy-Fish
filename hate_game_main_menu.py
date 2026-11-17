import pygame
import sys
import subprocess


pygame.init()

WIDTH, HEIGHT = 1350, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hate Game")
clock = pygame.time.Clock()


BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 160, 210)
TEXT_COLOR = (255, 255, 255)

font_title = pygame.font.SysFont("lucidaconsole", 70, bold=True)
font_button = pygame.font.SysFont("lucidaconsole", 36)

menu_bg = pygame.image.load("menu_bg.png").convert()
menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))


class Button:
    def __init__(self, text, center_x, center_y, width=260, height=60):
        self.text = text
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (center_x, center_y)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = BUTTON_HOVER if self.rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        pygame.draw.rect(surface, TEXT_COLOR, self.rect, 2, border_radius=12)
        text_surf = font_button.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


start_button = Button("Начать игру", WIDTH // 2, HEIGHT // 2)
exit_button = Button("Выход", WIDTH // 2, HEIGHT // 2 + 90)


def draw_menu():
    screen.blit(menu_bg, (0, 0))
    title = font_title.render("Hate Game", True, TEXT_COLOR)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 4)))
    start_button.draw(screen)
    exit_button.draw(screen)


def launch_game():
    pygame.quit()
    subprocess.run([sys.executable, "lvl_1.py"])
    sys.exit()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if start_button.is_clicked(event):
            launch_game()
        if exit_button.is_clicked(event):
            pygame.quit()
            sys.exit()


    draw_menu()
    pygame.display.flip()
    clock.tick(60)