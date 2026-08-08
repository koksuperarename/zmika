
import pygame
from menu import Menu

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змійка")

clock = pygame.time.Clock()

menu = Menu(screen)

state = "menu"
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == "menu":
                result = menu.click(event.pos)

                if result == "game":
                    state = "game"

                elif result == "exit":
                    running = False

    if state == "menu":
        menu.draw()

    elif state == "game":
        screen.fill((20, 20, 20))

        font = pygame.font.Font(None, 60)
        text = font.render("ТУТ БУДЕ ЗМІЙКА", True, (0, 255, 0))
        screen.blit(text, (230, 270))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
