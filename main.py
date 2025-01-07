import pygame
import os
import sys
import random

SIZE = WIDTH, HEIGHT = (1920, 1080)
MAX_WAVE = 20
TILE_SIZE_BOARD = 150
TILE_SIZE_SHOP = 145
DIR_SPAWN = 'spawn'
DIR_DATA = 'data'
LEFT_GAME_BOARD = 541
TOP_GAME_BOARD = 251
LEFT_SHOP = 845
TOP_SHOP = 37
FPS = 30


def load_image(name, directory, colorkey=None):
    fullname = os.path.join(directory, name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class BaseCharacter:
    def __init__(self, health, x, y, directory):
        self.health = health
        self.x = x
        self.y = y
        self.directory = directory

    def change_health(self, damage):
        self.health -= self.health - damage

    def is_alive(self):
        return self.health > 0

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen, left, top, tile):
        x = left + self.x * tile
        y = top + self.y * tile
        pygame.draw.rect(screen, pygame.Color('black'), (x, y, tile, tile))

    def __str__(self):
        return self.directory

    def __repr__(self):
        return str(self.directory)


class Settings:
    def __init__(self):
        self.start_money = 100
        self.hp = 20
        self.wave_delay = 120000
        self.enemies_for_waves = {
            1: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            2: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            3: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            4: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2],
            5: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2],
            6: [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2],
            7: [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2],
            8: [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2],
            9: [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2],
            10: [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2],
            11: [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2],
            12: [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
            13: [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
            14: [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
            15: [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
            16: [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
            17: [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
            18: [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
            19: [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
            20: [1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2]
        }

    class WaterTurret:
        def __init__(self):
            self.directory = 'bucket'
            self.health = 5
            self.delay = 5000
            self.cost = 100
            self.frames = {
                'atack': [],
                'motion': [],
                'die': [],
                'stop': ''
            }

    class WaterBullet:
        def __init__(self):
            self.directory = 'bucket_bullet'
            self.speed = 4
            self.damage = 1
            self.frames = {
                'motion': [],
                'stop': ''
            }

    class Generator:
        def __init__(self):
            self.directory = 'generator'
            self.health = 5
            self.delay = 10000
            self.cost = 50
            self.plus_cost = 25
            self.frames = {
                'atack': [],
                'motion': [],
                'die': [],
                'stop': ''
            }

    class Wall:
        def __init__(self):
            self.directory = 'wall'
            self.health = 8
            self.cost = 50
            self.frames = {
                'stop': ''
            }

    class Dino:
        def __init__(self):
            self.directory = 'dino'
            self.health = 5
            self.damage = 1
            self.delay = 3000
            self.speed = 0.2
            self.frames = {
                'atack': [],
                'motion': [],
                'die': [],
                'finish': [],
                'stop': load_image('Dino0.png', 'data/dino')
            }

    class Nail:
        def __init__(self):
            self.directory = 'nail'
            self.health = 10
            self.damage = 2
            self.delay = 4000
            self.speed = 0.1
            self.frames = {
                'atack': [],
                'motion': [],
                'die': [],
                'finish': [],
                'stop': ''
            }


class Board:
    # создание поля
    def __init__(self, width, height, left, top, tile_size):
        self.width = width
        self.height = height
        self.board = [[None] * width for _ in range(height)]
        # значения по умолчанию
        self.left = left
        self.top = top
        self.cell_size = tile_size

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if ((self.left > x or x > self.width * self.cell_size + self.left) or
                (self.top > y or y > self.height * self.cell_size + self.top)):
            return None
        cell_x = (x - self.left) // self.cell_size
        cell_y = (y - self.top) // self.cell_size
        return cell_y, cell_x


class GameBoard(Board):
    def __init__(self, width, height, left, top, tile_size):
        super().__init__(width, height, left, top, tile_size)

    def render(self, screen):
        for row in self.board:
            for unit in row:
                if unit is not None:
                    unit.render(screen, LEFT_GAME_BOARD, TOP_GAME_BOARD, TILE_SIZE_BOARD)

    def update(self, screen):
        for row in self.board:
            for unit in row:
                if unit is not None:
                    unit.update(screen)


class Shop(Board):
    def __init__(self, width, height, left, top, tile_size, units):
        super().__init__(width, height, left, top, tile_size)
        self.units = [*units]
        self.board[0] = [unit for unit in units] + [None, None, None]

    def on_click(self, cell):
        pass

    def get_unit(self, pos):
        x, y = pos
        return self.board[y][x]

    def render(self, screen):
        for row in self.board:
            for unit in row:
                if unit is not None:
                    unit.render(screen, LEFT_SHOP, TOP_SHOP, TILE_SIZE_SHOP)


class Bullet:
    def __init__(self, x, y, directory, bullet_speed, bullet_damage, frames):
        self.bullet_damage = bullet_damage
        self.bullet_speed = bullet_speed
        self.x = x
        self.y = y
        self.directory = directory
        self.frames = frames

    def set_bullet_damage(self, bullet_damage):
        self.bullet_damage = bullet_damage

    def set_bullet_speed(self, bullet_speed):
        self.bullet_speed = bullet_speed

    def get_bullet_speed(self):
        return self.bullet_speed

    def get_bullet_damage(self):
        return self.bullet_damage

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen):
        x, y = self.get_position()
        x = LEFT_GAME_BOARD + self.x * TILE_SIZE_BOARD
        y = TOP_GAME_BOARD + self.y * TILE_SIZE_BOARD
        pygame.draw.rect(screen, pygame.Color('white'), (x, y, TILE_SIZE_BOARD, TILE_SIZE_BOARD))

    def update(self):
        x, y = self.get_position()
        x += self.bullet_speed / FPS
        self.set_position(position=(x, y))


class Turret(BaseCharacter):
    def __init__(self, x, y, directory, cost, health, delay, bullet, frames):
        super().__init__(health, x, y, directory)
        self.delay = delay
        self.cost = cost
        self.bullet = bullet
        self.last_update_time = pygame.time.get_ticks()
        self.bullets = []
        self.frames = frames

    def copy(self, pos):
        return Turret(pos[1], pos[0], self.directory, self.cost, self.health, self.delay, self.bullet, self.frames)

    def update(self, screen):
        if self.bullets:
            for bullet in self.bullets:
                bullet.update()
                if bullet.get_position()[0] * TILE_SIZE_BOARD + LEFT_GAME_BOARD >= WIDTH:
                    try:
                        self.bullets.remove(bullet)
                    except ValueError as ve:
                        print(ve)
                bullet.render(screen)
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time >= self.delay:
            bullet = Settings.WaterBullet()
            self.bullets.append(
                self.bullet(self.x, self.y, bullet.directory, bullet.speed, bullet.damage, bullet.frames))
            self.last_update_time = current_time


class Wall(BaseCharacter):
    def __init__(self, x, y, directory, health, cost, frames):
        super().__init__(health, x, y, directory)
        self.cost = cost
        self.frames = frames

    def copy(self, pos):
        x, y = pos[1], pos[0]
        return Wall(x, y, self.directory, self.health, self.cost, self.frames)

    def update(self, screen):
        pass


class Generator(BaseCharacter):
    def __init__(self, x, y, directory, health, delay, plus_cost, cost, frames):
        super().__init__(health, x, y, directory)
        self.delay = delay
        self.plus_cost = plus_cost
        self.cost = cost
        self.frames = frames

    def copy(self, pos):
        return Generator(pos[1], pos[0], self.directory, self.health, self.delay, self.plus_cost, self.cost,
                         self.frames)

    def update(self, screen):
        pass


class Enemy(BaseCharacter):
    def __init__(self, x, y, directory, health, enemy_speed, damage, delay, frames):
        super().__init__(health, x, y, directory)
        self.damage = damage
        self.enemy_speed = enemy_speed
        self.delay = delay
        self.frames = frames


class Wave:
    def __init__(self, wave_counter, delay, enemy_matrix):
        self.counter = wave_counter
        self.delay = delay
        self.enemy_matrix = enemy_matrix
        self.current_enemies = []
        self.id = 0
        self.last_update = pygame.time.get_ticks()

    def start_wave(self):
        pass

    def finish_wave(self):
        pass

    def update(self):
        pass

    def render(self, screen):
        pass


class Spawn:
    def __init__(self, wave_counter, delay, enemies):
        self.wave_counter = wave_counter
        self.delay = delay
        self.last_update = pygame.time.get_ticks()
        self.start_game()
        self.enemies = enemies
        self.waves_dict = {i: self.generate_wave_matrix(i, enemies[i - 1]) for i in range(1, 21)}

    def get_wave_counter(self):
        return self.wave_counter

    def set_wave_counter(self, wave_counter):
        self.wave_counter = wave_counter

    def start_game(self):
        self.wave = Wave(0, 10000)

    def update(self, screen):
        # ведение волны
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.delay:
            self.set_wave_counter(self.get_wave_counter() + 1)
            self.wave.finish_wave()
            enemy_matrix = self.waves_dict[self.get_wave_counter() + 1]
            self.wave = Wave(self.get_wave_counter(), 10000, enemy_matrix)

        if self.wave_counter != 0:
            self.wave.update()

    def render(self, screen):
        pass

    def generate_wave_matrix(self, level, enemies):
        """Генерирует матрицу для заданной волны"""
        rows, cols = 5, 12
        matrix = [[0 for _ in range(cols)] for _ in range(rows)]
        num_enemies = level * 3

        # Заполняем каждый столбец хотя бы одним врагом
        for col in range(cols):
            row = random.randint(0, rows - 1)
            enemy_type = random.choice(enemies) if level > 1 else 1
            matrix[row][col] = enemy_type

        # Заполняем оставшиеся враги
        remaining_enemies = num_enemies - cols

        for _ in range(remaining_enemies):
            while True:
                row = random.randint(0, rows - 1)
                col = random.randint(0, cols - 1)
                if matrix[row][col] == 0:  # Если клетка пустая
                    # Случайно выбираем тип врага
                    enemy_type = random.choice(enemies) if level > 1 else 1
                    matrix[row][col] = enemy_type
                    break

        return matrix


class Game:
    def __init__(self, game_board, shop, settings):
        self.game_board = game_board
        self.shop = shop
        self.settings = settings
        self.total_money = settings.start_money
        self.wave_delay = settings.wave_delay
        self.enemies_for_spawn = settings.enemies_for_waves
        self.hp = settings.hp
        self.wave_counter = 0
        self.is_hold = False
        self.current_unit = None
        self.spawn = Spawn(self.wave_counter, self.wave_delay, self.enemies_for_spawn)

    def create_unit(self, pos, unit):
        return unit.copy(pos)

    def render(self, screen):
        self.game_board.render(screen)

    def is_win(self):
        pass

    def is_lose(self):
        pass

    def get_click(self, mouse_pos, up):
        game_board_cell = self.game_board.get_cell(mouse_pos)
        shop_cell = self.shop.get_cell(mouse_pos)

        if game_board_cell:
            y, x = game_board_cell
            if self.current_unit is not None and self.is_hold:
                # создаем юнита в клетке, отвязываем спрайт от курсора
                self.game_board.board[y][x] = self.create_unit(game_board_cell, self.current_unit)
                self.is_hold = False
                self.current_unit = None

        elif shop_cell:
            y, x = shop_cell
            if not up:
                if self.current_unit is not self.shop.get_unit((x, y)):

                    self.current_unit = self.shop.get_unit((x, y))
                    self.is_hold = True
                    # привязка спрайта к курсору
                else:
                    self.is_hold = False
                    self.current_unit = None

        else:
            self.is_hold = False
            self.current_unit = None

    def update(self, screen):
        self.game_board.update(screen)


def init_shop(settings: Settings):
    result = []

    gen = settings.Generator()
    generator = Generator(0, 0, gen.directory, gen.health, gen.delay, gen.plus_cost, gen.cost, gen.frames)
    result.append(generator)

    wt = settings.WaterTurret()
    watter_turret = Turret(1, 0, wt.directory, wt.cost, wt.health, wt.delay, Bullet, wt.frames)
    result.append(watter_turret)

    wll = settings.Wall()
    wall = Wall(2, 0, wll.directory, wll.health, wll.cost, wll.frames)
    result.append(wall)

    return result


def main():
    # инициализация игры
    pygame.init()

    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('АТЕ')
    pygame.mouse.set_visible(False)

    background_image = load_image('background.png', DIR_DATA)
    cursor_image = load_image("cursor.png", "data/cursor")

    settings = Settings()

    units_for_shop = init_shop(settings)

    game_board = GameBoard(9, 5, LEFT_GAME_BOARD, TOP_GAME_BOARD, TILE_SIZE_BOARD)
    shop = Shop(6, 1, LEFT_SHOP, TOP_SHOP, TILE_SIZE_SHOP, units_for_shop)
    game = Game(game_board, shop, settings)

    running = True
    game_paused = False
    clock = pygame.time.Clock()
    # игровой цикл
    while running:
        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    game_paused = not game_paused
                    continue
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.get_click(event.pos, False)
            if event.type == pygame.MOUSEBUTTONUP:
                game.get_click(event.pos, True)
            if event.type == pygame.MOUSEMOTION:
                # добавить рамку в магазин
                mouse_coord = event.pos

        if not game_paused:
            screen.blit(background_image, (0, 0))
            game.update(screen)
            game.render(screen)

        if pygame.mouse.get_focused():
            screen.blit(cursor_image, mouse_coord)

        clock.tick(FPS)
        pygame.display.flip()


if __name__ == '__main__':
    main()
