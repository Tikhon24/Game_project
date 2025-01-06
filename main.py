import pygame
import os
import sys

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

    def __str__(self):
        return self.directory

    def __repr__(self):
        return str(self.directory)


class Settings:
    def __init__(self):
        self.start_money = 100
        self.hp = 20

    class WaterTurret:
        def __init__(self):
            self.directory = 'bucket'
            self.health = 5
            self.delay = 5000
            self.cost = 100

    class WaterBullet:
        def __init__(self):
            self.directory = 'bucket_bullet'
            self.speed = 1
            self.damage = 1

    class Generator:
        def __init__(self):
            self.directory = 'generator'
            self.health = 5
            self.delay = 10000
            self.cost = 50
            self.plus_cost = 25

    class Wall:
        def __init__(self):
            self.directory = 'wall'
            self.health = 8
            self.cost = 50


class Board:
    # создание поля
    def __init__(self, width, height, left, top, tile_size):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = left
        self.top = top
        self.cell_size = tile_size

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        color = pygame.Color('white')
        for row in range(self.height):
            y = self.top + row * self.cell_size
            for col in range(self.width):
                x = self.left + col * self.cell_size
                pygame.draw.rect(screen, color, (x, y, self.cell_size, self.cell_size), width=1)

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

    def on_click(self, cell):
        pass


class Shop(Board):
    def __init__(self, width, height, left, top, tile_size, units):
        super().__init__(width, height, left, top, tile_size)
        self.units = [*units]
        self.board[0] = [unit for unit in units] + [0, 0, 0]

    def on_click(self, cell):
        pass

    def get_unit(self, pos):
        x, y = pos
        return self.board[y][x]


class Bullet:
    def __init__(self, bullet_speed=1, bullet_damage=1):
        self.bullet_damage = bullet_damage
        self.bullet_speed = bullet_speed

    def set_bullet_damage(self, bullet_damage):
        self.bullet_damage = bullet_damage

    def set_bullet_speed(self, bullet_speed):
        self.bullet_speed = bullet_speed


class Turret(BaseCharacter):
    def __init__(self, x, y, directory, cost, health, delay):
        super().__init__(health, x, y, directory)
        self.delay = delay
        self.cost = cost


class Wall(BaseCharacter):
    def __init__(self, x, y, directory, health, cost):
        super().__init__(health, x, y, directory)
        self.cost = cost


class Generator(BaseCharacter):
    def __init__(self, x, y, directory, health, delay, plus_cost, cost):
        super().__init__(health, x, y, directory)
        self.delay = delay
        self.plus_cost = plus_cost
        self.cost = cost


class Enemy(BaseCharacter):
    def __init__(self, x, y, directory, health=5, enemy_speed=0.2, damage=1, delay=3000):
        super().__init__(health, x, y, directory)
        self.damage = damage
        self.enemy_speed = enemy_speed
        self.delay = delay


class Wave:
    pass


class Spawn:
    pass


class Game:
    def __init__(self, game_board, shop, settings):
        self.game_board = game_board
        self.shop = shop
        self.settings = settings
        self.total_money = settings.start_money
        self.hp = settings.hp
        self.wave_counter = 0
        self.is_hold = False
        self.current_unit = None

    def create_unit(self, pos, unit):
        x, y = pos
        self.game_board.board[y][x] = unit(x, y)

    def render(self, screen):
        self.game_board.render(screen)
        self.shop.render(screen)

    def is_win(self):
        pass

    def is_lose(self):
        pass

    def get_click(self, mouse_pos, up):
        if not up:
            self.is_hold = False

        game_board_cell = self.game_board.get_cell(mouse_pos)
        shop_cell = self.shop.get_cell(mouse_pos)

        if game_board_cell:
            y, x = game_board_cell
            if self.current_unit is not None and self.is_hold:
                # создаем юнита в клетке, отвязываем спрайт от курсора
                self.game_board.board[y][x] = self.create_unit(self.current_unit)

        elif shop_cell:
            if not up:
                y, x = shop_cell
                self.current_unit = self.shop.get_unit((x, y))
                self.is_hold = True
                # привязка спрайта к курсору

        else:
            self.is_hold = False
            self.current_unit = None


def init_shop(settings: Settings):
    result = []

    gen = settings.Generator()
    generator = Generator(0, 0, gen.directory, gen.health, gen.delay, gen.plus_cost, gen.cost)
    result.append(generator)

    wt = settings.WaterTurret()
    watter_turret = Turret(0, 0, wt.directory, wt.cost, wt.health, wt.delay)
    result.append(watter_turret)

    wll = settings.Wall()
    wall = Wall(0, 0, wll.directory, wll.health, wll.cost)
    result.append(wall)

    return result


def main():
    # инициализация игры
    pygame.init()

    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('АТЕ')

    background_image = load_image('background.png', DIR_DATA)

    settings = Settings()

    units_for_shop = init_shop(settings)

    game_board = Board(9, 5, LEFT_GAME_BOARD, TOP_GAME_BOARD, TILE_SIZE_BOARD)
    shop = Shop(6, 1, LEFT_SHOP, TOP_SHOP, TILE_SIZE_SHOP, units_for_shop)
    game = Game(game_board, shop, settings)

    print(shop.units)

    running = True
    game_paused = False
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

        if not game_paused:
            screen.blit(background_image, (0, 0))
            game.render(screen)
            pygame.display.flip()


if __name__ == '__main__':
    main()
