
import pygame
import random


class Menu:

    def __init__(self, screen):

        self.screen = screen

        # Шрифти
        self.title_font = pygame.font.Font(None, 100)
        self.button_font = pygame.font.Font(None, 50)
        self.small_font = pygame.font.Font(None, 30)

        # Кнопки
        self.play_button = pygame.Rect(250, 250, 300, 80)
        self.exit_button = pygame.Rect(250, 350, 300, 80)

        self.button_radius = 15

        # ---------------- ЧАСТИНКИ ----------------

        self.particles = []

        for i in range(70):

            particle = {
                "x": random.randint(0, 800),
                "y": random.randint(0, 600),

                "size": random.randint(4, 14),

                "speed_x": random.uniform(-0.7, 0.7),
                "speed_y": random.uniform(-0.7, 0.7),

                "color": (
                    random.randint(0, 50),
                    random.randint(100, 255),
                    random.randint(30, 120)
                )
            }

            self.particles.append(particle)

    # ---------------- ФОН ----------------

    def draw_background(self):

        self.screen.fill((10, 15, 10))

        # Сітка
        for x in range(0, 800, 40):

            pygame.draw.line(
                self.screen,
                (15, 35, 15),
                (x, 0),
                (x, 600)
            )

        for y in range(0, 600, 40):

            pygame.draw.line(
                self.screen,
                (15, 35, 15),
                (0, y),
                (800, y)
            )

        # ---------------- ЛІТАЮЧІ ЧАСТИНКИ ----------------

        for particle in self.particles:

            # Рух
            particle["x"] += particle["speed_x"]
            particle["y"] += particle["speed_y"]

            # Якщо вилетіли за екран —
            # повертаємо з іншого боку
            if particle["x"] < -20:
                particle["x"] = 820

            if particle["x"] > 820:
                particle["x"] = -20

            if particle["y"] < -20:
                particle["y"] = 620

            if particle["y"] > 620:
                particle["y"] = -20

            # Малюємо частинку
            pygame.draw.rect(
                self.screen,
                particle["color"],
                (
                    int(particle["x"]),
                    int(particle["y"]),
                    particle["size"],
                    particle["size"]
                ),
                border_radius=4
            )

    # ---------------- ЗАГОЛОВОК ----------------

    def draw_title(self):

        # Тінь
        shadow = self.title_font.render(
            "ЗМІЙКА",
            True,
            (0, 60, 0)
        )

        shadow_rect = shadow.get_rect(
            center=(404, 154)
        )

        self.screen.blit(
            shadow,
            shadow_rect
        )

        # Заголовок
        title = self.title_font.render(
            "ЗМІЙКА",
            True,
            (0, 255, 80)
        )

        title_rect = title.get_rect(
            center=(400, 145)
        )

        self.screen.blit(
            title,
            title_rect
        )

    # ---------------- КНОПКА ----------------

    def draw_button(self, button, text, color):

        mouse_pos = pygame.mouse.get_pos()

        hovered = button.collidepoint(mouse_pos)

        if hovered:

            button_color = (
                min(color[0] + 50, 255),
                min(color[1] + 50, 255),
                min(color[2] + 50, 255)
            )

            # Світіння
            glow = button.inflate(12, 12)

            pygame.draw.rect(
                self.screen,
                (30, 70, 30),
                glow,
                border_radius=20
            )

        else:

            button_color = color

        # Кнопка
        pygame.draw.rect(
            self.screen,
            button_color,
            button,
            border_radius=self.button_radius
        )

        # Рамка
        pygame.draw.rect(
            self.screen,
            (150, 255, 150),
            button,
            2,
            border_radius=self.button_radius
        )

        # Текст
        text_surface = self.button_font.render(
            text,
            True,
            (255, 255, 255)
        )

        text_rect = text_surface.get_rect(
            center=button.center
        )

        self.screen.blit(
            text_surface,
            text_rect
        )

    # ---------------- МЕНЮ ----------------

    def draw(self):

        self.draw_background()

        self.draw_title()

        self.draw_button(
            self.play_button,
            "ГРАТИ",
            (0, 150, 60)
        )

        self.draw_button(
            self.exit_button,
            "ВИХІД",
            (170, 30, 30)
        )

        # Інформація
        info = self.small_font.render(
            "WASD / Стрілки — керування",
            True,
            (120, 150, 120)
        )

        info_rect = info.get_rect(
            center=(400, 500)
        )

        self.screen.blit(
            info,
            info_rect
        )

        # Версія
        version = self.small_font.render(
            "SNAKE GAME",
            True,
            (60, 80, 60)
        )

        self.screen.blit(
            version,
            (20, 570)
        )

    # ---------------- КЛІК ----------------

    def click(self, pos):

        if self.play_button.collidepoint(pos):
            return "game"

        if self.exit_button.collidepoint(pos):
            return "exit"

        return "menu"