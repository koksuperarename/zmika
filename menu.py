
import pygame


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 70)
        self.button_font = pygame.font.Font(None, 50)

        self.play_button = pygame.Rect(250, 250, 300, 80)
        self.exit_button = pygame.Rect(250, 350, 300, 80)

    def draw(self):
        self.screen.fill((30, 30, 30))

        title = self.font.render("ЗМІЙКА", True, (0, 255, 0))
        self.screen.blit(title, (300, 100))

        pygame.draw.rect(self.screen, (0, 180, 0), self.play_button)
        pygame.draw.rect(self.screen, (180, 0, 0), self.exit_button)

        play_text = self.button_font.render("ГРАТИ", True, (255, 255, 255))
        exit_text = self.button_font.render("ВИХІД", True, (255, 255, 255))

        self.screen.blit(play_text, (330, 270))
        self.screen.blit(exit_text, (335, 370))

    def click(self, pos):
        if self.play_button.collidepoint(pos):
            return "game"

        if self.exit_button.collidepoint(pos):
            return "exit"

        return "menu"

