import json

import pygame
import os
import sys
import random

from settings import Settings
from units import Bullet, Turret, Generator, Wall, Enemy, Swamp
from units import all_units, all_bullets, all_enemies

pygame.mixer.init()
# -=----------------------------------=-
FONT = "data/font/yellwa.ttf"
SIZE = WIDTH, HEIGHT = (1920, 1080)
MAX_WAVE = 20
TILE_SIZE_BOARD = 150
TILE_SIZE_SHOP = 145
DIR_DATA = 'data'
SCORE = f'{DIR_DATA}/score/score.json'
LEFT_GAME_BOARD = 541
TOP_GAME_BOARD = 251
LEFT_SHOP = 845
TOP_SHOP = 37
FPS = 30
SOUNDS = {
    "shopping": pygame.mixer.Sound('data/sound/shopping.mp3'),
    "ban": pygame.mixer.Sound('data/sound/ban.mp3')
}

settings = Settings()


class Statistics:
    def __init__(self):
        self.data = self.load_score(SCORE)

    def load_score(self, filename):
        with open(filename, 'r') as file:
            return json.load(file)

    def get_data(self):
        return self.data

    def clean_current_data(self):
        # очистка сессионных значений, не трогаем значения за всё время
        for key in ['enemy_killed', 'unit_killed', 'time', 'money']:
            self.data[key] = 0

    def upload_score(self, filename):
        self.clean_current_data()
        with open(filename, 'w') as file:
            json.dump(self.get_data(), file)

    def up_enemy_killed(self):
        self.data['enemy_killed'] += 1
        self.data['all_enemy_killed'] += 1

    def up_unit_killed(self):
        self.data['unit_killed'] += 1
        self.data['all_unit_killed'] += 1

    def up_time(self, time):
        current_time = self.data['time']
        new_time = time - current_time
        self.data['time'] += new_time
        self.data['all_time'] += new_time

    def up_money(self, money):
        self.data['money'] += money
        self.data['all_money'] += money


statistics = Statistics()


def load_image(name, directory, colorkey=None):
    fullname = os.path.join(directory, name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def render_text(screen, text, font_size, coords, color=(0, 130, 149)):
    font = pygame.font.Font(FONT, font_size)
    text_surface = font.render(str(text), True, pygame.Color(color))
    screen.blit(text_surface, coords)


def terminate():
    statistics.upload_score(SCORE)
    pygame.quit()
    sys.exit()


def start_screen(screen, clock, coords):
    menu = load_image('menu.png', f'{DIR_DATA}/screen').convert_alpha()
    cursor_image = pygame.transform.scale(load_image("cursor.png", "data/cursor").convert_alpha(), (50, 50))
    screen.blit(menu, (0, 0))

    mouse_coord = coords

    while True:
        screen.blit(menu, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                mouse_coord = event.pos
            # -=-------------------=BUTTONS=-------------------=-
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                # play
                if 110 <= pos[0] <= 430 and 70 <= pos[1] <= 240:
                    # start game
                    return mouse_coord
                # credits
                if 90 <= pos[0] <= 420 and 260 <= pos[1] <= 380:
                    pass
                # soon
                if 78 <= pos[0] <= 425 and 410 <= pos[1] <= 565:
                    pass
                # exit
                if 68 <= pos[0] <= 428 and 596 <= pos[1] <= 745:
                    terminate()
            # -=-----------------------------------------------=-

        if pygame.mouse.get_focused():
            screen.blit(cursor_image, mouse_coord)

        clock.tick(FPS)
        pygame.display.flip()


def finsh_screen(screen, clock, is_win):
    if is_win:
        background = load_image('winground.png', f'{DIR_DATA}/screen').convert_alpha()
        color = (0, 103, 139)
    else:
        background = load_image('dieground.png', f'{DIR_DATA}/screen').convert_alpha()
        color = (213, 213, 0)
    cursor_image = pygame.transform.scale(load_image("cursor.png", "data/cursor").convert_alpha(), (50, 50))
    screen.blit(background, (0, 0))

    mouse_coord = (0, 0)

    while True:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                mouse_coord = event.pos
            # -=-------------------=BUTTONS=-------------------=-
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if 0 <= pos[0] <= 250 and 1000 <= pos[1] <= 1080:
                    return mouse_coord
            # -=-----------------------------------------------=-

        # -=---------------------------------=STATISTIC=---------------------------------=-
        stat = statistics.get_data()
        render_text(screen, stat["time"] // 60000, 32, (1797, 620), color)
        render_text(screen, stat["enemy_killed"], 32, (1795, 722), color)
        render_text(screen, stat["unit_killed"], 32, (1795, 840), color)
        render_text(screen, stat["money"], 32, (1795, 965), color)
        # -=---------------------------------=--------------------------------------------=-

        if pygame.mouse.get_focused():
            screen.blit(cursor_image, mouse_coord)

        clock.tick(FPS)
        pygame.display.flip()


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

    def update(self):
        for y in range(self.height):
            for x in range(self.width):
                unit = self.board[y][x]
                if unit:
                    if unit.is_deleted:
                        self.input_unit(x, y, None)


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


class Wave:
    def __init__(self, wave_counter, delay, enemy_matrix, statistics):
        self.counter = wave_counter
        self.delay = delay
        self.enemy_matrix = enemy_matrix
        self.statistics = statistics
        self.id = 0
        self.last_update = pygame.time.get_ticks()
        self.relations_enemies = {
            0: None,
            1: settings.enemy_relation['dino'],
            2: settings.enemy_relation['nail']
        }
        self.count_of_spawn = 0

    def start_wave(self):
        pass

    def finish_wave(self):
        pass

    def create_enemy(self, enemy_type, pos):
        params = enemy_type
        x, y = pos
        all_enemies.add(
            Enemy(x, y, params.directory, params.health, params.speed, params.damage, params.delay, params.frames,
                  self.statistics))

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


class Spawn:
    def __init__(self, wave_counter, delay, enemies, statistics):
        self.wave_counter = wave_counter
        self.waves_dict = {i: self.generate_wave_matrix(i, enemies[i]) for i in range(1, 21)}
        self.waves_dict[21] = [None]
        self.delay = delay
        self.last_update = pygame.time.get_ticks()
        self.enemies = enemies
        self.statistics = statistics
        self.wave = Wave(self.wave_counter, 10000, None, self.statistics)
        # self.wave = Wave(self.wave_counter, 10000, self.waves_dict[self.get_wave_counter()], self.statistics)

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
            if self.wave_counter == 21:
                return
            enemy_matrix = self.waves_dict[self.get_wave_counter()]
            self.wave = Wave(self.get_wave_counter(), 10000, enemy_matrix, self.statistics)
            self.last_update = current_time
        self.wave.update()

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
    def __init__(self, game_board: GameBoard, shop, swamp, settings, statistics):
        self.game_board = game_board
        self.shop = shop
        self.swamp = swamp
        self.settings = settings
        self.statistics = statistics
        self.total_money = settings.start_money
        self.wave_delay = settings.wave_delay
        self.enemies_for_spawn = settings.enemies_for_waves
        self.hp = settings.hp
        self.wave_counter = 0
        self.is_hold = False
        self.current_unit = None
        self.spawn = Spawn(self.wave_counter, self.wave_delay, self.enemies_for_spawn, self.statistics)
        # self.spawn = Spawn(20, self.wave_delay, self.enemies_for_spawn, self.statistics)

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
        if self.spawn.wave_counter == 21 and len(all_enemies) == 0:
            return True
        return False

    def is_lose(self):
        if self.hp <= 0:
            return True
        return False

    def get_click(self, mouse_pos, up):
        game_board_cell = self.game_board.get_cell(mouse_pos)
        shop_cell = self.shop.get_cell(mouse_pos)

        if game_board_cell:
            y, x = game_board_cell
            if self.current_unit is not None and self.is_hold:
                # создаем юнита в клетке, отвязываем спрайт от курсора
                if self.game_board.board[y][x] is None:
                    self.total_money -= self.current_unit.cost
                    unit = self.create_unit(game_board_cell, self.current_unit)
                    self.game_board.input_unit(x, y, unit)
                    all_units.add(unit)
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

    def change_hp(self, damage):
        self.hp -= damage

    def update(self):
        self.spawn.update()
        self.game_board.update()

        all_enemies.update()

        units = all_units.sprites()
        for i in range(len(units)):
            if isinstance(units[i], Generator):
                plus_money = units[i].update()
                self.total_money += plus_money
                self.statistics.up_money(plus_money)
            else:
                units[i].update()

        all_bullets.update()

        damage = self.swamp.update()
        if damage:
            self.change_hp(damage)


def init_shop(settings: Settings, statistics):
    result = []

    gen = settings.Generator()
    generator = Generator(0, 0, gen.directory, gen.health, gen.delay, gen.plus_cost, gen.cost, gen.frames, statistics)
    result.append(generator)

    wt = settings.WaterTurret()
    watter_turret = Turret(1, 0, wt.directory, wt.cost, wt.health, wt.delay, Bullet, wt.frames, statistics)
    result.append(watter_turret)

    wll = settings.Wall()
    wall = Wall(2, 0, wll.directory, wll.health, wll.cost, wll.frames, statistics)
    result.append(wall)

    return result


def main():
    # инициализация игры
    pygame.init()

    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('АТЕ')
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    background_image = load_image('background.png', f'{DIR_DATA}/screen').convert_alpha()
    pauseground_image = load_image('pauseground.png', f'{DIR_DATA}/screen').convert_alpha()
    pause_btn_image = load_image('pause.png', f'{DIR_DATA}/buttons').convert_alpha()
    into_menu_btn_image = pygame.transform.scale(load_image('into_menu.png', f'{DIR_DATA}/buttons').convert_alpha(),
                                                 (75, 75))
    cursor_image = pygame.transform.scale(load_image("cursor.png", "data/cursor").convert_alpha(), (50, 50))

    units_for_shop = init_shop(settings, statistics)
    # загрузка спрайтов врагов
    settings.enemy_relation = {
        'dino': settings.Dino(),
        'nail': settings.Nail()
    }

    game_board = GameBoard(9, 5, LEFT_GAME_BOARD, TOP_GAME_BOARD, TILE_SIZE_BOARD)
    shop = Shop(3, 1, LEFT_SHOP, TOP_SHOP, TILE_SIZE_SHOP, units_for_shop)
    swamp = Swamp()
    game = Game(game_board, shop, swamp, settings, statistics)

    running = True
    game_paused = False

    mouse_coord = start_screen(screen, clock, (0, 0))

    # игровой цикл
    while running:
        if game.is_win():
            mouse_coord = finsh_screen(screen, clock, True)
            mouse_coord = start_screen(screen, clock, mouse_coord)

        if game.is_lose():
            mouse_coord = finsh_screen(screen, clock, False)
            mouse_coord = start_screen(screen, clock, mouse_coord)

        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = False
                    mouse_coord = start_screen(screen, clock, mouse_coord)
                    continue
                if event.key == pygame.K_p:
                    game_paused = not game_paused
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game_paused:
                    game.get_click(event.pos, False)
            if event.type == pygame.MOUSEBUTTONUP:
                pos = event.pos
                # settings_btn
                if 15 <= pos[0] <= 90 and 990 <= pos[1] <= 1065:
                    game_paused = False
                    mouse_coord = start_screen(screen, clock, mouse_coord)
                    continue
                elif not game_paused:
                    game.get_click(event.pos, True)
                else:
                    if 885 <= pos[0] <= 1035 and 465 <= pos[1] <= 615:
                        game_paused = not game_paused

            if event.type == pygame.MOUSEMOTION:
                # добавить рамку в магазин
                mouse_coord = event.pos

        if not game_paused:
            game.update()
        screen.blit(background_image, (0, 0))
        screen.blit(into_menu_btn_image, (15, 990))
        game.render(screen)

        if game_paused:
            screen.blit(pauseground_image, (0, 0))
            screen.blit(pause_btn_image, (885, 465))
            screen.blit(into_menu_btn_image, (15, 990))
            game.is_hold = False
            game.current_unit = None
            for enemy in all_enemies:
                enemy.last_update += 1000 / clock.get_fps()
            for unit in all_units:
                if not isinstance(unit, Wall):
                    unit.last_update += 1000 / clock.get_fps()

        # fps
        font = pygame.font.SysFont('Arial', 24)
        fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))

        if pygame.mouse.get_focused():
            if game.is_hold:
                screen.blit(game.current_unit.image, (mouse_coord[0] - 75, mouse_coord[-1] - 75))
            screen.blit(cursor_image, mouse_coord)
        clock.tick(FPS)
        statistics.up_time(pygame.time.get_ticks())
        pygame.display.flip()


if __name__ == '__main__':
    main()
