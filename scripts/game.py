import random

import pygame

from scripts import tools


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 0
        self.top = 50
        self.cell_size = 50

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen: pygame.Surface):
        for row in range(self.width):
            for col in range(self.height):
                if self.board[col][row] == 1:  # 1 - змея
                    pygame.draw.rect(screen, pygame.Color('Green'),
                                     (row * self.cell_size + self.left, col * self.cell_size + self.top,
                                      self.cell_size, self.cell_size), 0)
                elif self.board[col][row] == 2:  # 2 - яблоко
                    pygame.draw.rect(screen, pygame.Color('Red'),
                                     (row * self.cell_size + self.left, col * self.cell_size + self.top,
                                      self.cell_size, self.cell_size), 0)
                pygame.draw.rect(screen, pygame.Color((150, 150, 150)),
                                 (row * self.cell_size + self.left, col * self.cell_size + self.top,
                                  self.cell_size, self.cell_size), 1)

    def drop_board(self):
        self.board = [[0] * self.width for _ in range(self.height)]

    def set_cell(self, x, y, type):
        self.board[x][y] = type


class SnakePiece:
    def __init__(self, pos_x: int, pos_y: int):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def get_coords(self) -> tuple[int, int]:
        return self.pos_x, self.pos_y

    def check_collisions(self, objects: list) -> bool:
        for i in objects:
            if self.check_collision(i):
                return True
        return False

    def check_collision(self, object):
        return self.pos_x == object.get_coords()[0] and self.pos_y == object.get_coords()[1]


def correct_coords(x: int, y: int):
    # игровое поле 16 на 16
    return 0 <= x < 16 and 0 <= y < 16


def game_scene(screen: pygame.Surface, switch_scene):
    running = True
    board = Board(16, 16)
    apples_count = 0
    # ограничение по фпс
    clock = pygame.time.Clock()
    fps = 8
    max_apple = tools.get_statistic()
    snake = [SnakePiece(8, 8), SnakePiece(8, 7)]  # список-очередь для всех объектов змейки
    direction = -1  # 0 - влево, 1 - вверх, 2 - вправо, 3 - вниз
    is_growth = False
    while True:
        apple = SnakePiece(random.randint(0, 15), random.randint(0, 15))
        if not apple.check_collisions(snake):
            break
    font = pygame.font.SysFont('Comic Sans MS', 36)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tools.save_statistic(max_apple=apples_count)
                running = False
                switch_scene(None)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = 0
                elif event.key == pygame.K_UP:
                    direction = 1
                elif event.key == pygame.K_RIGHT:
                    direction = 2
                elif event.key == pygame.K_DOWN:
                    direction = 3
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    switch_scene("Menu")
                    tools.save_statistic(max_apple=apples_count)

        if apple.check_collision(snake[-1]):
            is_growth = True
            apples_count += 1
            while True:
                apple = SnakePiece(random.randint(0, 15), random.randint(0, 15))
                if not apple.check_collisions(snake):
                    break

        if direction != -1:
            x = snake[-1].pos_x
            y = snake[-1].pos_y
            if direction == 0:
                y -= 1
            elif direction == 1:
                x -= 1
            elif direction == 2:
                y += 1
            elif direction == 3:
                x += 1
            if correct_coords(x, y):
                piece = SnakePiece(x, y)
                if piece.check_collisions(snake):
                    tools.save_statistic(max_apple=apples_count)
                    running = False
                snake.append(piece)
                if not is_growth:
                    snake.pop(0)
                is_growth = False
            else:
                tools.save_statistic(max_apple=apples_count)
                running = False

        screen.fill((0, 0, 0))
        board.drop_board()
        board.set_cell(*apple.get_coords(), 2)

        max_apple = max(max_apple, apples_count)
        text = font.render(f"Apple: {apples_count}", True, (255, 255, 255))
        max_text = font.render(f"Max apple: {max_apple}", True, (255, 255, 255))
        screen.blit(text, (50, 0))
        screen.blit(max_text, (500, 0))
        for i in snake:
            board.set_cell(*i.get_coords(), 1)
        board.render(screen)
        pygame.display.flip()
        clock.tick(fps)
