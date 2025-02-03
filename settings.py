import pygame
import sys
import os

TILE_SIZE_BOARD = 150


def load_image(name, directory, colorkey=None):
    fullname = os.path.join(directory, name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


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
                'stop': pygame.transform.scale(load_image("Shape0.png", "data/shape"),
                                               (TILE_SIZE_BOARD, TILE_SIZE_BOARD))
            }

    class WaterBullet:
        def __init__(self):
            self.directory = 'bucket_bullet'
            self.speed = 3.5
            self.damage = 1
            self.frames = {
                'motion': [
                    pygame.transform.scale(load_image(f'Bul{i}.png', 'data/bullet'), (TILE_SIZE_BOARD, TILE_SIZE_BOARD))
                    for i in range(11)
                ],
                'stop': pygame.transform.scale(load_image("Bul0.png", "data/bullet"),
                                               (TILE_SIZE_BOARD, TILE_SIZE_BOARD))
            }

    class Generator:
        def __init__(self):
            self.directory = 'generator'
            self.health = 5
            # self.delay = 10000
            self.delay = 100
            self.cost = 50
            self.plus_cost = 25
            self.frames = {
                'atack': [],
                'motion': [],
                'die': [],
                'stop': pygame.transform.scale(load_image("Rustik0.png", "data/rustik"),
                                               (TILE_SIZE_BOARD, TILE_SIZE_BOARD))
            }

    class Wall:
        def __init__(self):
            self.directory = 'wall'
            self.health = 8
            self.cost = 50
            self.frames = {
                'stop': pygame.transform.scale(load_image("Aqueduct.png", "data/aqueduct"),
                                               (TILE_SIZE_BOARD, TILE_SIZE_BOARD))
            }

    class Dino:
        def __init__(self):
            self.directory = 'dino'
            self.health = 5
            self.damage = 1
            self.delay = 3000
            self.speed = 0.2
            self.frames = {
                'atack': [
                    pygame.transform.scale(load_image(f'Bul{i}.png', 'data/bullet'), (TILE_SIZE_BOARD, TILE_SIZE_BOARD))
                    for i in range(11)
                ],
                'motion': [],
                'die': [],
                'finish': [],
                'stop': pygame.transform.scale(load_image('dino.png', 'data/dino'), (TILE_SIZE_BOARD, TILE_SIZE_BOARD))
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
                'stop': pygame.transform.scale(load_image('Nail0.png', 'data/nail'), (TILE_SIZE_BOARD, TILE_SIZE_BOARD))
            }
