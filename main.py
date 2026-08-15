import pygame
import random

from menu import Menu


# =========================================================
# ІНІЦІАЛІЗАЦІЯ
# =========================================================

pygame.init()


# =========================================================
# РОЗМІР ЕКРАНУ
# =========================================================

WIDTH = 800
HEIGHT = 600

CELL_SIZE = 20

HUD_HEIGHT = 70

GAME_TOP = HUD_HEIGHT


screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "Змійка"
)


clock = pygame.time.Clock()

menu = Menu(screen)


# =========================================================
# КОЛЬОРИ
# =========================================================

BACKGROUND = (8, 13, 10)

PANEL_COLOR = (15, 25, 18)

GREEN = (40, 220, 90)
LIGHT_GREEN = (100, 255, 140)
DARK_GREEN = (20, 120, 50)

RED = (235, 45, 50)
LIGHT_RED = (255, 130, 130)

WHITE = (240, 245, 240)

GRAY = (130, 145, 135)

GRID_COLOR = (15, 28, 18)

WALL_COLOR = (30, 220, 80)

OBSTACLE_COLOR = (45, 75, 55)
OBSTACLE_BORDER = (90, 190, 100)

BLACK = (5, 10, 7)


# =========================================================
# ШРИФТИ
# =========================================================

font_small = pygame.font.Font(
    None,
    28
)

font_medium = pygame.font.Font(
    None,
    38
)

font_game_over = pygame.font.Font(
    None,
    80
)


# =========================================================
# ЗМІЙКА
# =========================================================

snake = []


direction = [
    CELL_SIZE,
    0
]


# Швидкість змійки
MOVE_DELAY = 120

last_move = 0


# =========================================================
# ЇЖА
# =========================================================

food = [
    0,
    0
]


# =========================================================
# ПЕРЕШКОДИ
# =========================================================

OBSTACLE_COUNT = 30

obstacles = []


# =========================================================
# ЖИТТЯ
# =========================================================

MAX_LIVES = 3

lives = MAX_LIVES


# =========================================================
# РАХУНОК
# =========================================================

score = 0


# =========================================================
# СТАН
# =========================================================

state = "menu"

running = True


# =========================================================
# СТВОРЕННЯ ЗМІЙКИ
# =========================================================

def reset_snake():

    global snake
    global direction
    global last_move

    snake = [
        [400, 320],
        [380, 320],
        [360, 320]
    ]

    direction = [
        CELL_SIZE,
        0
    ]

    last_move = pygame.time.get_ticks()


# =========================================================
# СТВОРЕННЯ ПЕРЕШКОД
# =========================================================

def create_obstacles():

    global obstacles

    obstacles = []

    possible_positions = []

    # Створюємо список усіх клітинок
    for x in range(
        0,
        WIDTH,
        CELL_SIZE
    ):

        for y in range(
            GAME_TOP,
            HEIGHT,
            CELL_SIZE
        ):

            position = [
                x,
                y
            ]

            # Не ставимо біля старту змійки
            if (
                abs(x - 400) < 140
                and abs(y - 320) < 120
            ):
                continue

            # Не ставимо на змійку
            if position in snake:
                continue

            possible_positions.append(
                position
            )

    # Перемішуємо
    random.shuffle(
        possible_positions
    )

    # Беремо потрібну кількість
    obstacles = possible_positions[
        :OBSTACLE_COUNT
    ]


# =========================================================
# СТВОРЕННЯ ЇЖІ
# =========================================================

def create_food():

    possible_positions = []

    for x in range(
        0,
        WIDTH,
        CELL_SIZE
    ):

        for y in range(
            GAME_TOP,
            HEIGHT,
            CELL_SIZE
        ):

            position = [
                x,
                y
            ]

            # Не можна на змійці
            if position in snake:
                continue

            # Не можна на перешкоді
            if position in obstacles:
                continue

            possible_positions.append(
                position
            )

    if len(possible_positions) > 0:

        return random.choice(
            possible_positions
        )

    # Запасний варіант
    return [
        CELL_SIZE,
        GAME_TOP + CELL_SIZE
    ]


# =========================================================
# НОВА ГРА
# =========================================================

def start_new_game():

    global lives
    global score
    global food

    lives = MAX_LIVES

    score = 0

    # Спочатку створюємо змійку
    reset_snake()

    # Потім перешкоди
    create_obstacles()

    # Потім їжу
    food = create_food()


# =========================================================
# ПЕРЕВІРКА ЗІТКНЕННЯ ЗІ СТІНОЮ
# =========================================================

def hit_wall(position):

    x = position[0]
    y = position[1]

    # Ліва стіна
    if x < 0:
        return True

    # Права стіна
    if x + CELL_SIZE > WIDTH:
        return True

    # Верхня стіна
    if y < GAME_TOP:
        return True

    # Нижня стіна
    if y + CELL_SIZE > HEIGHT:
        return True

    return False


# =========================================================
# ПЕРЕВІРКА ПЕРЕШКОД
# =========================================================

def hit_obstacle(position):

    snake_rect = pygame.Rect(
        position[0],
        position[1],
        CELL_SIZE,
        CELL_SIZE
    )

    for obstacle in obstacles:

        obstacle_rect = pygame.Rect(
            obstacle[0],
            obstacle[1],
            CELL_SIZE,
            CELL_SIZE
        )

        if snake_rect.colliderect(
            obstacle_rect
        ):
            return True

    return False


# =========================================================
# ПЕРЕВІРКА ВЛАСНОГО ТІЛА
# =========================================================

def hit_self(position, eating_food):

    head_rect = pygame.Rect(
        position[0],
        position[1],
        CELL_SIZE,
        CELL_SIZE
    )

    # Якщо яблуко НЕ їмо,
    # хвіст цього ходу забереться.
    body = snake

    if not eating_food and len(snake) > 1:

        body = snake[:-1]

    for part in body:

        body_rect = pygame.Rect(
            part[0],
            part[1],
            CELL_SIZE,
            CELL_SIZE
        )

        if head_rect.colliderect(
            body_rect
        ):
            return True

    return False


# =========================================================
# РУХ ЗМІЙКИ
# =========================================================

def move_snake():

    global snake
    global food
    global score

    # Нова позиція голови
    new_head = [
        snake[0][0] + direction[0],
        snake[0][1] + direction[1]
    ]


    # =====================================================
    # СТІНА
    # =====================================================

    if hit_wall(new_head):

        return False


    # =====================================================
    # ПЕРЕШКОДА
    # =====================================================

    if hit_obstacle(new_head):

        return False


    # =====================================================
    # ПЕРЕВІРКА ЇЖІ
    # =====================================================

    head_rect = pygame.Rect(
        new_head[0],
        new_head[1],
        CELL_SIZE,
        CELL_SIZE
    )

    food_rect = pygame.Rect(
        food[0],
        food[1],
        CELL_SIZE,
        CELL_SIZE
    )

    eating_food = head_rect.colliderect(
        food_rect
    )


    # =====================================================
    # ВЛАСНИЙ ХВІСТ
    # =====================================================

    if hit_self(
        new_head,
        eating_food
    ):

        return False


    # =====================================================
    # ДОДАЄМО ГОЛОВУ
    # =====================================================

    snake.insert(
        0,
        new_head
    )


    # =====================================================
    # ЯБЛУКО
    # =====================================================

    if eating_food:

        # +10 очок
        score += 10

        # Нове яблуко
        food = create_food()

        # Хвіст НЕ видаляємо.
        # Тому змійка збільшується.

    else:

        # Звичайний рух
        snake.pop()


    return True


# =========================================================
# ФОН
# =========================================================

def draw_background():

    screen.fill(
        BACKGROUND
    )

    # Вертикальна сітка
    for x in range(
        0,
        WIDTH,
        CELL_SIZE
    ):

        pygame.draw.line(
            screen,
            GRID_COLOR,
            (x, GAME_TOP),
            (x, HEIGHT)
        )

    # Горизонтальна сітка
    for y in range(
        GAME_TOP,
        HEIGHT,
        CELL_SIZE
    ):

        pygame.draw.line(
            screen,
            GRID_COLOR,
            (0, y),
            (WIDTH, y)
        )

    # =====================================================
    # СТІНИ
    # =====================================================

    # Верх
    pygame.draw.line(
        screen,
        WALL_COLOR,
        (0, GAME_TOP),
        (WIDTH, GAME_TOP),
        4
    )

    # Ліва
    pygame.draw.line(
        screen,
        WALL_COLOR,
        (0, GAME_TOP),
        (0, HEIGHT),
        4
    )

    # Права
    pygame.draw.line(
        screen,
        WALL_COLOR,
        (WIDTH - 1, GAME_TOP),
        (WIDTH - 1, HEIGHT),
        4
    )

    # Нижня
    pygame.draw.line(
        screen,
        WALL_COLOR,
        (0, HEIGHT - 1),
        (WIDTH, HEIGHT - 1),
        4
    )


# =========================================================
# HUD
# =========================================================

def draw_hud():

    pygame.draw.rect(
        screen,
        PANEL_COLOR,
        (
            0,
            0,
            WIDTH,
            HUD_HEIGHT
        )
    )

    # Нижня лінія HUD
    pygame.draw.line(
        screen,
        DARK_GREEN,
        (
            0,
            HUD_HEIGHT - 1
        ),
        (
            WIDTH,
            HUD_HEIGHT - 1
        ),
        2
    )


    # =====================================================
    # НАЗВА
    # =====================================================

    title = font_medium.render(
        "ЗМІЙКА",
        True,
        GREEN
    )

    screen.blit(
        title,
        (25, 17)
    )


    # =====================================================
    # РАХУНОК
    # =====================================================

    score_text = font_small.render(
        f"Рахунок: {score}",
        True,
        WHITE
    )

    score_rect = score_text.get_rect(
        center=(
            WIDTH // 2,
            35
        )
    )

    screen.blit(
        score_text,
        score_rect
    )


    # =====================================================
    # ЖИТТЯ
    # =====================================================

    lives_text = font_small.render(
        "Життя:",
        True,
        WHITE
    )

    screen.blit(
        lives_text,
        (610, 25)
    )

    for i in range(
        MAX_LIVES
    ):

        x = 700 + i * 27

        if i < lives:

            draw_heart(
                x,
                35,
                RED
            )

        else:

            draw_heart(
                x,
                35,
                (50, 55, 50)
            )


# =========================================================
# СЕРДЕЧКО
# =========================================================

def draw_heart(
    x,
    y,
    color
):

    pygame.draw.circle(
        screen,
        color,
        (
            x - 5,
            y - 3
        ),
        6
    )

    pygame.draw.circle(
        screen,
        color,
        (
            x + 5,
            y - 3
        ),
        6
    )

    pygame.draw.polygon(
        screen,
        color,
        [
            (x - 11, y),
            (x + 11, y),
            (x, y + 12)
        ]
    )


# =========================================================
# ЗМІЙКА
# =========================================================

def draw_snake():

    for i, part in enumerate(
        snake
    ):

        x = part[0]
        y = part[1]

        rect = pygame.Rect(
            x + 2,
            y + 2,
            CELL_SIZE - 4,
            CELL_SIZE - 4
        )


        # =================================================
        # ГОЛОВА
        # =================================================

        if i == 0:

            pygame.draw.rect(
                screen,
                LIGHT_GREEN,
                rect,
                border_radius=6
            )

            # Очі
            pygame.draw.circle(
                screen,
                BLACK,
                (
                    x + 7,
                    y + 7
                ),
                2
            )

            pygame.draw.circle(
                screen,
                BLACK,
                (
                    x + 14,
                    y + 7
                ),
                2
            )


        # =================================================
        # ТІЛО
        # =================================================

        else:

            pygame.draw.rect(
                screen,
                GREEN,
                rect,
                border_radius=5
            )

            # Блік
            pygame.draw.rect(
                screen,
                (90, 245, 125),
                (
                    x + 5,
                    y + 5,
                    4,
                    4
                ),
                border_radius=2
            )


# =========================================================
# ЯБЛУКО
# =========================================================

def draw_food():

    x = food[0] + CELL_SIZE // 2
    y = food[1] + CELL_SIZE // 2


    # Світіння
    pygame.draw.circle(
        screen,
        (70, 15, 20),
        (
            x,
            y
        ),
        12
    )


    # Яблуко
    pygame.draw.circle(
        screen,
        RED,
        (
            x,
            y + 1
        ),
        8
    )


    # Блік
    pygame.draw.circle(
        screen,
        LIGHT_RED,
        (
            x - 3,
            y - 3
        ),
        2
    )


    # Стебло
    pygame.draw.line(
        screen,
        (100, 60, 25),
        (
            x,
            y - 7
        ),
        (
            x + 2,
            y - 12
        ),
        2
    )


    # Листочок
    pygame.draw.ellipse(
        screen,
        GREEN,
        (
            x + 2,
            y - 13,
            7,
            4
        )
    )


# =========================================================
# ПЕРЕШКОДИ
# =========================================================

def draw_obstacles():

    for obstacle in obstacles:

        x = obstacle[0]
        y = obstacle[1]


        # =================================================
        # ТІНЬ
        # =================================================

        shadow = pygame.Rect(
            x + 3,
            y + 4,
            CELL_SIZE - 3,
            CELL_SIZE - 3
        )

        pygame.draw.rect(
            screen,
            (5, 10, 7),
            shadow,
            border_radius=5
        )


        # =================================================
        # ОСНОВНА ПЕРЕШКОДА
        # =================================================

        rect = pygame.Rect(
            x + 1,
            y + 1,
            CELL_SIZE - 2,
            CELL_SIZE - 2
        )

        pygame.draw.rect(
            screen,
            OBSTACLE_COLOR,
            rect,
            border_radius=5
        )


        # =================================================
        # ОБВОДКА
        # =================================================

        pygame.draw.rect(
            screen,
            OBSTACLE_BORDER,
            rect,
            2,
            border_radius=5
        )


        # =================================================
        # БЛІК
        # =================================================

        pygame.draw.line(
            screen,
            (140, 230, 150),
            (
                x + 5,
                y + 5
            ),
            (
                x + 13,
                y + 5
            ),
            2
        )


# =========================================================
# КЕРУВАННЯ
# =========================================================

def draw_controls():

    text = font_small.render(
        "WASD / СТРІЛКИ — рух    ESC — меню",
        True,
        GRAY
    )

    rect = text.get_rect(
        center=(
            WIDTH // 2,
            HEIGHT - 12
        )
    )

    screen.blit(
        text,
        rect
    )


# =========================================================
# GAME OVER
# =========================================================

def draw_game_over():

    overlay = pygame.Surface(
        (
            WIDTH,
            HEIGHT
        ),
        pygame.SRCALPHA
    )

    overlay.fill(
        (0, 0, 0, 180)
    )

    screen.blit(
        overlay,
        (0, 0)
    )


    # GAME OVER
    text = font_game_over.render(
        "GAME OVER",
        True,
        RED
    )

    text_rect = text.get_rect(
        center=(
            WIDTH // 2,
            245
        )
    )

    screen.blit(
        text,
        text_rect
    )


    # Рахунок
    score_text = font_medium.render(
        f"Рахунок: {score}",
        True,
        WHITE
    )

    score_rect = score_text.get_rect(
        center=(
            WIDTH // 2,
            320
        )
    )

    screen.blit(
        score_text,
        score_rect
    )


# =========================================================
# ГОЛОВНИЙ ЦИКЛ
# =========================================================

while running:

    # =====================================================
    # ПОДІЇ
    # =====================================================

    for event in pygame.event.get():

        # Закриття
        if event.type == pygame.QUIT:

            running = False


        # =================================================
        # МИША
        # =================================================

        if event.type == pygame.MOUSEBUTTONDOWN:

            if state == "menu":

                result = menu.click(
                    event.pos
                )

                if result == "game":

                    state = "game"

                    start_new_game()

                elif result == "exit":

                    running = False


        # =================================================
        # КЛАВІАТУРА
        # =================================================

        if event.type == pygame.KEYDOWN:

            if state == "game":


                # -----------------------------------------
                # ВГОРУ
                # -----------------------------------------

                if (
                    event.key == pygame.K_UP
                    or event.key == pygame.K_w
                ):

                    # Не можна розвернутися назад
                    if direction != [
                        0,
                        CELL_SIZE
                    ]:

                        direction = [
                            0,
                            -CELL_SIZE
                        ]


                # -----------------------------------------
                # ВНИЗ
                # -----------------------------------------

                elif (
                    event.key == pygame.K_DOWN
                    or event.key == pygame.K_s
                ):

                    if direction != [
                        0,
                        -CELL_SIZE
                    ]:

                        direction = [
                            0,
                            CELL_SIZE
                        ]


                # -----------------------------------------
                # ВЛІВО
                # -----------------------------------------

                elif (
                    event.key == pygame.K_LEFT
                    or event.key == pygame.K_a
                ):

                    if direction != [
                        CELL_SIZE,
                        0
                    ]:

                        direction = [
                            -CELL_SIZE,
                            0
                        ]


                # -----------------------------------------
                # ВПРАВО
                # -----------------------------------------

                elif (
                    event.key == pygame.K_RIGHT
                    or event.key == pygame.K_d
                ):

                    if direction != [
                        -CELL_SIZE,
                        0
                    ]:

                        direction = [
                            CELL_SIZE,
                            0
                        ]


                # -----------------------------------------
                # ESC
                # -----------------------------------------

                elif event.key == pygame.K_ESCAPE:

                    state = "menu"


    # =====================================================
    # МЕНЮ
    # =====================================================

    if state == "menu":

        menu.draw()


    # =====================================================
    # ГРА
    # =====================================================

    elif state == "game":

        # Фон + стіни
        draw_background()

        # HUD
        draw_hud()


        # =================================================
        # РУХ
        # =================================================

        current_time = pygame.time.get_ticks()

        if (
            current_time - last_move
            >= MOVE_DELAY
        ):

            alive = move_snake()


            # =============================================
            # ЗІТКНЕННЯ
            # =============================================

            if not alive:

                # Мінус одне життя
                lives -= 1


                # =========================================
                # GAME OVER
                # =========================================

                if lives <= 0:

                    draw_obstacles()

                    draw_food()

                    draw_snake()

                    draw_game_over()

                    pygame.display.flip()

                    pygame.time.delay(
                        1500
                    )

                    state = "menu"


                # =========================================
                # ЩЕ Є ЖИТТЯ
                # =========================================

                else:

                    # Відродження
                    reset_snake()

                    # Перегенеровуємо їжу,
                    # щоб вона не опинилася
                    # на новій змійці
                    food = create_food()


            last_move = current_time


        # =================================================
        # МАЛЮВАННЯ
        # =================================================

        if state == "game":

            draw_obstacles()

            draw_food()

            draw_snake()

            draw_controls()


    # =====================================================
    # ОНОВЛЕННЯ
    # =====================================================

    pygame.display.flip()

    clock.tick(60)


# =========================================================
# ВИХІД
# =========================================================

pygame.quit()