import pygame
import os
import sys
import random

pygame.mixer.init()
# -=----------------------------------=-
FONT = "data/font/yellwa.ttf"
SIZE = WIDTH, HEIGHT = (1920, 1080)
MAX_WAVE = 20
TILE_SIZE_BOARD = 150
TILE_SIZE_SHOP = 145
DIR_DATA = 'data'
LEFT_GAME_BOARD = 541
TOP_GAME_BOARD = 251
LEFT_SHOP = 845
TOP_SHOP = 37
FPS = 30
SOUNDS = {
    "shopping": pygame.mixer.Sound('data/sound/shopping.mp3'),
    "ban": pygame.mixer.Sound('data/sound/ban.mp3')
}
# -=----------------------------------=-
all_bullets = pygame.sprite.Group()
all_enemies = pygame.sprite.Group()
all_units = pygame.sprite.Group()
# -=----------------------------------=-


def load_image(name, directory, colorkey=None):
    fullname = os.path.join(directory, name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def render_text(screen, text, font_size, coords):
    font = pygame.font.Font(FONT, font_size)
    text_surface = font.render(str(text), True, pygame.Color(0, 130, 149))
    screen.blit(text_surface, coords)


def terminate():
    pygame.quit()
    sys.exit()


class BaseCharacter(pygame.sprite.Sprite):
    def __init__(self, health, x, y, directory):
        super().__init__()
        self.health = health
        self.x = x
        self.y = y
        self.directory = directory

    def change_health(self, damage):
        self.health -= damage

    def is_alive(self):
        return self.health > 0

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        x, y = position
        self.x, self.y = x, y
        self.rect.x, self.rect.y = LEFT_GAME_BOARD + x * TILE_SIZE_BOARD, TOP_GAME_BOARD + y * TILE_SIZE_BOARD

    def render(self, screen):
        x, y = self.get_position()
        x = LEFT_GAME_BOARD + x * TILE_SIZE_BOARD
        y = TOP_GAME_BOARD + y * TILE_SIZE_BOARD
        screen.blit(pygame.transform.scale(self.image, (TILE_SIZE_BOARD, TILE_SIZE_BOARD)), (x, y))

    def kill(self):
        self.health = 0
        del self

    def __str__(self):
        return self.directory

    def __repr__(self):
        return str(self.directory)


class Settings:
    """Игровые настройки"""

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
                'stop': load_image("backly.png", "data/backly")
            }

    class WaterBullet:
        def __init__(self):
            self.directory = 'bucket_bullet'
            self.speed = 3.5
            self.damage = 1
            self.frames = {
                'motion': [],
                'stop': pygame.transform.scale(load_image("bullet.png", "data/bucket_bullet"),
                                               (TILE_SIZE_BOARD, TILE_SIZE_BOARD))
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
                'stop': load_image("dino0.png", "data/dino")
            }

    class Wall:
        def __init__(self):
            self.directory = 'wall'
            self.health = 8
            self.cost = 50
            self.frames = {
                'stop': load_image("dino0.png", "data/dino")
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
                'stop': pygame.transform.scale(load_image('Dino0.png', 'data/dino'), (TILE_SIZE_BOARD, TILE_SIZE_BOARD))
            }

    class Nail:
        def __init__(self):
            self.directory = 'nail'
            self.health = 10
            self.damage = 2
            self.delay = 4000
            self.speed = 0.15
            self.frames = {
                'atack': [],
                'motion': [],
                'die': [],
                'finish': [],
                'stop': pygame.transform.scale(load_image('Dino0.png', 'data/dino'), (TILE_SIZE_BOARD, TILE_SIZE_BOARD))
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

    def input_unit(self, x, y, unit):
        self.board[y][x] = unit


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


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, directory, bullet_speed, bullet_damage, frames):
        super().__init__(all_bullets)
        self.bullet_damage = bullet_damage
        self.bullet_speed = bullet_speed
        self.x = x
        self.y = y
        self.directory = directory
        self.frames = frames
        self.image = self.frames['stop']
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

    def kill(self):
        self.health = 0
        del self

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
        x, y = position
        self.x, self.y = x, y
        self.rect.x, self.rect.y = LEFT_GAME_BOARD + x * TILE_SIZE_BOARD, TOP_GAME_BOARD + y * TILE_SIZE_BOARD

    def set_mask(self):
        self.mask = pygame.mask.from_surface(self.image)

    def render(self, screen):
        x, y = self.get_position()
        x = LEFT_GAME_BOARD + x * TILE_SIZE_BOARD
        y = TOP_GAME_BOARD + y * TILE_SIZE_BOARD
        screen.blit(pygame.transform.scale(self.image, (TILE_SIZE_BOARD, TILE_SIZE_BOARD)), (x, y))

    def update(self):
        enemy = pygame.sprite.spritecollideany(self, all_enemies)
        if enemy:
            print(self.rect)
            print(enemy.rect)
            damage = self.get_bullet_damage()
            enemy.change_health(damage)
            # удаление объектов, если они больше не являются частью игры
            if not enemy.is_alive():
                all_enemies.remove(enemy)
                enemy.kill()
            all_bullets.remove(self)
            self.image = load_image('cursor.png', 'data/cursor')

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
        self.frames = frames
        self.image = self.frames['stop']
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.flag = True

    def copy(self, pos):
        return Turret(pos[1], pos[0], self.directory, self.cost, self.health, self.delay, self.bullet, self.frames)

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time >= self.delay and self.flag:
            # self.flag = False
            bullet = Settings.WaterBullet()
            my_bullet = self.bullet(self.x, self.y, bullet.directory, bullet.speed, bullet.damage, bullet.frames)
            all_bullets.add(my_bullet)
            self.last_update_time = current_time


class Wall(BaseCharacter):
    def __init__(self, x, y, directory, health, cost, frames):
        super().__init__(health, x, y, directory)
        self.cost = cost
        self.frames = frames
        self.image = self.frames['stop']
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

    def copy(self, pos):
        x, y = pos[1], pos[0]
        return Wall(x, y, self.directory, self.health, self.cost, self.frames)

    def update(self):
        pass


class Generator(BaseCharacter):
    def __init__(self, x, y, directory, health, delay, plus_cost, cost, frames):
        super().__init__(health, x, y, directory)
        self.delay = delay
        self.plus_cost = plus_cost
        self.cost = cost
        self.last_update_time = pygame.time.get_ticks()
        self.frames = frames
        self.image = self.frames['stop']
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

    def copy(self, pos):
        return Generator(pos[1], pos[0], self.directory, self.health, self.delay, self.plus_cost, self.cost,
                         self.frames)

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time >= self.delay:
            self.last_update_time = current_time
            return self.plus_cost
        return 0


class Enemy(BaseCharacter):
    def __init__(self, x, y, directory, health, enemy_speed, damage, delay, frames):
        super().__init__(health, x, y, directory)
        self.damage = damage
        self.enemy_speed = enemy_speed
        self.delay = delay
        self.frames = frames
        self.image = self.frames['stop']
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.last_update = pygame.time.get_ticks()

    def set_mask(self):
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.delay:
            self.last_update = current_time
        x, y = self.get_position()
        x -= self.enemy_speed / FPS
        self.set_position(position=(x, y))


class Wave:
    def __init__(self, wave_counter, delay, enemy_matrix):
        self.counter = wave_counter
        self.delay = delay
        self.enemy_matrix = enemy_matrix
        self.current_enemies = []
        self.id = 0
        self.last_update = pygame.time.get_ticks()
        self.relations_enemies = {
            0: None,
            1: Settings.Dino,
            2: Settings.Nail
        }
        self.count_of_spawn = 0

    def start_wave(self):
        pass

    def finish_wave(self):
        pass

    def create_enemy(self, enemy_type, pos):
        params = enemy_type()
        x, y = pos
        all_enemies.add(
            Enemy(x, y, params.directory, params.health, params.speed, params.damage, params.delay, params.frames))

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.delay:
            if self.enemy_matrix:
                self.count_of_spawn += 1
                enemies_to_spawn = [row[self.count_of_spawn - 1] for row in self.enemy_matrix]
                x = 10
                for y, id in enumerate(enemies_to_spawn):
                    match id:
                        case 0:
                            pass
                        case _:
                            self.create_enemy(self.relations_enemies[id], pos=(x, y))
            self.last_update = current_time

    def render(self, screen):
        for enemy in self.current_enemies:
            enemy.render(screen)


class Spawn:
    def __init__(self, wave_counter, delay, enemies):
        self.wave_counter = wave_counter
        self.waves_dict = {i: self.generate_wave_matrix(i, enemies[i]) for i in range(1, 21)}
        self.delay = delay
        self.last_update = pygame.time.get_ticks()
        self.enemies = enemies
        self.current_enemies = []
        # self.wave = Wave(self.wave_counter, 10000, None)
        self.wave = Wave(self.wave_counter, 10000, self.waves_dict[self.get_wave_counter()])

    def get_wave_counter(self):
        return self.wave_counter

    def set_wave_counter(self, wave_counter):
        self.wave_counter = wave_counter

    def update(self):
        # ведение волны
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.delay:
            self.set_wave_counter(self.get_wave_counter() + 1)
            self.wave.finish_wave()
            enemy_matrix = self.waves_dict[self.get_wave_counter()]
            self.wave = Wave(self.get_wave_counter(), 10000, enemy_matrix)
            self.last_update = current_time

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
        # self.spawn = Spawn(self.wave_counter, self.wave_delay, self.enemies_for_spawn)
        self.spawn = Spawn(2, self.wave_delay, self.enemies_for_spawn)

    def create_unit(self, pos, unit):
        return unit.copy(pos)

    def render(self, screen):
        for unit in all_units:
            unit.render(screen)
        for enemy in all_enemies:
            enemy.render(screen)
        for bullet in all_bullets:
            bullet.render(screen)
        render_text(screen, self.total_money, 36, (425, 80))
        render_text(screen, self.hp, 48, (95, 15))

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
                if self.game_board.board[y][x] is None:
                    self.total_money -= self.current_unit.cost
                    self.game_board.board[y][x] = self.create_unit(game_board_cell, self.current_unit)
                    SOUNDS["shopping"].play()
                else:
                    SOUNDS["ban"].play()
                self.is_hold = False
                self.current_unit = None

        elif shop_cell:
            y, x = shop_cell
            if not up:
                if self.current_unit is not self.shop.get_unit((x, y)):
                    self.current_unit = self.shop.get_unit((x, y))
                    if self.current_unit.cost <= self.total_money:
                        self.is_hold = True
                        # привязка спрайта к курсору
                    else:
                        SOUNDS["ban"].play()
                        self.is_hold = False
                        self.current_unit = None
                else:
                    self.is_hold = False
                    self.current_unit = None

        else:
            self.is_hold = False
            self.current_unit = None

    def update(self):
        self.spawn.update()

        enemies = all_enemies.sprites()
        for i in range(len(enemies)):
            enemies[i].update()

        units = all_units.sprites()
        for i in range(len(units)):
            if isinstance(units[i], Generator):
                self.total_money += units[i].update()
            else:
                units[i].update()

        bullets = all_bullets.sprites()
        for i in range(len(bullets)):
            bullets[i].update()


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
    clock = pygame.time.Clock()

    background_image = load_image('background.png', DIR_DATA)
    cursor_image = load_image("cursor.png", "data/cursor")

    settings = Settings()

    units_for_shop = init_shop(settings)

    game_board = GameBoard(9, 5, LEFT_GAME_BOARD, TOP_GAME_BOARD, TILE_SIZE_BOARD)
    shop = Shop(6, 1, LEFT_SHOP, TOP_SHOP, TILE_SIZE_SHOP, units_for_shop)
    game = Game(game_board, shop, settings)

    running = True
    game_paused = False

    mouse_coord = (0, 0)
    # игровой цикл
    while running:
        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
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
            game.update()
            game.render(screen)

        if pygame.mouse.get_focused():
            screen.blit(cursor_image, mouse_coord)

        clock.tick(FPS)
        pygame.display.flip()


if __name__ == '__main__':
    main()
