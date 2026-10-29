"""Игра «Змейка» на pygame.

Модуль содержит базовый класс GameObject, яблоко, змейку,
обработчик клавиш и основной игровой цикл.
"""

from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Клавиши управления и противоположные направления:
KEY_DIRECTIONS = {
    pygame.K_UP: UP,
    pygame.K_w: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_s: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_a: LEFT,
    pygame.K_RIGHT: RIGHT,
    pygame.K_d: RIGHT,
}
OPPOSITE_DIRECTIONS = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT,
}

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки:
BORDER_COLOR = (93, 216, 228)

# Цвет яблока:
APPLE_COLOR = (255, 0, 0)

# Цвет змейки:
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32
)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый игровой объект, занимающий одну клетку поля."""

    def __init__(self, position=None, body_color=(255, 255, 255)):
        """Создать объект в клетке position с цветом body_color."""
        self.position = position or (0, 0)
        self.body_color = body_color

    def draw(self):
        """Нарисовать объект в его текущей клетке."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Яблоко, которое змейка собирает на поле."""

    def __init__(self, position=None, body_color=APPLE_COLOR):
        """Создать яблоко и разместить его на случайной клетке."""
        super().__init__(position, body_color)
        self.randomize_position()

    def randomize_position(self, occupied_positions=None):
        """Переместить яблоко в случайную свободную клетку."""
        occupied = set(occupied_positions or ())
        free_cells = [
            (x, y)
            for x in range(0, SCREEN_WIDTH, GRID_SIZE)
            for y in range(0, SCREEN_HEIGHT, GRID_SIZE)
            if (x, y) not in occupied
        ]
        if free_cells:
            self.position = choice(free_cells)
        else:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
        return self.position

    def draw(self):
        """Нарисовать яблоко."""
        super().draw()


class Snake(GameObject):
    """Змейка, управляемая стрелками или клавишами WASD."""

    def __init__(self, position=None, body_color=SNAKE_COLOR):
        """Создать змейку из трёх сегментов в центре поля."""
        super().__init__(position, body_color)
        self.reset()

    def reset(self):
        """Вернуть змейку в начальное состояние."""
        center_x = (GRID_WIDTH // 2) * GRID_SIZE
        center_y = (GRID_HEIGHT // 2) * GRID_SIZE
        self.positions = [
            (center_x, center_y),
            (center_x - GRID_SIZE, center_y),
            (center_x - 2 * GRID_SIZE, center_y),
        ]
        self.position = self.positions[0]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Вернуть координаты головы змейки."""
        return self.positions[0]

    def next_head_position(self):
        """Вернуть клетку, в которую переместится голова змейки."""
        head_x, head_y = self.get_head_position()
        delta_x, delta_y = self.direction
        return head_x + delta_x * GRID_SIZE, head_y + delta_y * GRID_SIZE

    def update_direction(self):
        """Применить отложенное направление после нажатия клавиши."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, grow=False):
        """Переместить змейку на одну клетку.

        Если grow=True, хвост не удаляется и змейка растёт.
        Возвращает False при столкновении со стеной или собой.
        """
        new_head = self.next_head_position()
        head_x, head_y = new_head
        hit_wall = not (
            0 <= head_x < SCREEN_WIDTH
            and 0 <= head_y < SCREEN_HEIGHT
        )
        occupied = self.positions if grow else self.positions[:-1]
        hit_self = new_head in occupied
        if hit_wall or hit_self:
            return False

        self.positions.insert(0, new_head)
        self.position = new_head
        if grow:
            self.last = None
        else:
            self.last = self.positions.pop()
        return True

    def draw(self):
        """Нарисовать тело, голову и стереть ушедший хвост."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(
            self.get_head_position(), (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(
                screen, BOARD_BACKGROUND_COLOR, last_rect
            )


def handle_keys(game_object):
    """Обработать события клавиатуры и изменить направление змейки."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type != pygame.KEYDOWN:
            continue
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            raise SystemExit
        direction = KEY_DIRECTIONS.get(event.key)
        if direction is None:
            continue
        if game_object.direction != OPPOSITE_DIRECTIONS[direction]:
            game_object.next_direction = direction


def main():
    """Запустить игру «Змейка»."""
    pygame.init()
    snake = Snake()
    apple = Apple()
    apple.randomize_position(snake.positions)
    score = 0
    font = pygame.font.Font(None, 36)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()

        grow = snake.next_head_position() == apple.position
        if not snake.move(grow=grow):
            snake.reset()
            apple.randomize_position(snake.positions)
            score = 0
            continue

        if grow:
            score += 1
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        score_text = font.render(
            f'Score: {score}', True, (255, 255, 255)
        )
        screen.blit(score_text, (10, 10))
        pygame.display.update()


if __name__ == '__main__':
    main()
