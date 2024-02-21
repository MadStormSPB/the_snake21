"""Return the pathname of the KOS root directory."""
from random import randint

import pygame


# Инициализация PyGame:
pygame.init()

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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Стартовая позиция змейки:
SNAKE_START_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш.

    Измненение направления движения змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


class GameObject():
    """Абстрактный класс будущих игровых объектов."""

    def __init__(self, position=SNAKE_START_POSITION,
                 body_color=BOARD_BACKGROUND_COLOR):
        """Устанавливаем базовые положение и цвет объекта."""
        self.position = position
        self.body_color = body_color
        self.border_color = BORDER_COLOR

    def draw(self):
        """Абстрактный клас для отрисовки."""
        pass

    def draw_cell(self, position, surface):
        """Отрисовка клетки."""
        cell = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, cell)
        pygame.draw.rect(surface, self.border_color, cell, 1)

    def delete_cell(self, position, surface):
        """Закрашивание клетки."""
        cell_for_del = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, cell_for_del)


class Snake(GameObject):
    """Класс описывающий змею."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Устанавливаем позицию начал и цвет змеи."""
        super().__init__(body_color=body_color)
        self.reset()

    def update_direction(self):
        """Обновление направления движение головы змеи."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещение головы змеи(добавление в список нового элемента)."""
        dx, dy = self.direction
        head_x, head_y = self.get_head_position()
        self.positions.insert(
            0,
            (
                (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
                (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
            )
        )
        if self.length == len(self.positions) - 1:
            self.last = self.positions.pop(-1)

    def draw(self, surface):
        """Отрисовка змеи."""
        # Затирание хвоста змеи
        if self.last:
            self.delete_cell(self.last, screen)
        # Отрисовка головы змеи
        self.draw_cell(self.get_head_position(), screen)

    def get_head_position(self):
        """Метод для получения координат головы змеи."""
        return self.positions[0]

    def reset(self):
        """Перезапуск игры."""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.next_direction = LEFT
        self.last = None
        self.length = 1
        self.positions = [SNAKE_START_POSITION]
        self.direction = None


class Apple(GameObject):
    """Класс для игрового объекта - яблочка."""

    def __init__(self, body_color=APPLE_COLOR):
        """Создается яблоко на случайной позиции."""
        super().__init__(body_color=body_color)
        self.randomize_position()

    def randomize_position(self, taked_positions=[SNAKE_START_POSITION]):
        """Выдаём яблочку случайную позицию."""
        while self.position in taked_positions:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        """Функция отрисовки яблока."""
        super().draw_cell(self.position, surface)


def main():
    """Логика игрового процесса : главный игровой цикл."""
    snake = Snake()
    apple = Apple()
    apple.draw(screen)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()
            apple.draw(screen)
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
            apple.draw(screen)
        pygame.display.update()
        snake.draw(screen)


if __name__ == '__main__':
    main()