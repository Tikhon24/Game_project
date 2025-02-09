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
                'atack': [
                    pygame.transform.scale(load_image(f'Shape{i}.png', 'data/shape').convert_alpha(), (TILE_SIZE_BOARD, TILE_SIZE_BOARD))
                    for i in range(11)
                ],
                'motion': [],
                'die': [],
                'stop': pygame.transform.scale(load_image("Shape0.png", "data/shape").convert_alpha(),
                                               (TILE_SIZE_BOARD, TILE_SIZE_BOARD))
            }

    class WaterBullet:
        def __init__(self):
            self.directory = 'bucket_bullet'
            self.speed = 3.5
            self.damage = 1
            self.frames = {
                'motion': [
                    pygame.transform.scale(load_image(f'Bul{i}.png', 'data/bullet').convert_alpha(), (TILE_SIZE_BOARD, TILE_SIZE_BOARD))
                    for i in range(11)
                ],
                'stop': pygame.transform.scale(load_image("Bul0.png", "data/bullet").convert_alpha(),
                                               (TILE_SIZE_BOARD, TILE_SIZE_BOARD))
            }

    class Generator:
        def __init__(self):
            self.directory = 'generator'
            self.health = 5
            # self.delay = 10000
            self.delay = 3000
            self.cost = 50
            self.plus_cost = 25
            self.frames = {
                'atack': [
                    pygame.transform.scale(load_image(f'Rustik{i}.png', 'data/rustik').convert_alpha(), (TILE_SIZE_BOARD, TILE_SIZE_BOARD))
                    for i in range(10)
                ],
                'motion': [],
                'die': [],
                'stop': pygame.transform.scale(load_image("Rustik0.png", "data/rustik").convert_alpha(),
                                               (TILE_SIZE_BOARD, TILE_SIZE_BOARD))
            }

    class Wall:
        def __init__(self):
            self.directory = 'wall'
            self.health = 8
            self.cost = 70
            self.frames = {
                'stop': pygame.transform.scale(load_image("Aqueduct.png", "data/aqueduct").convert_alpha(),
                                               (TILE_SIZE_BOARD, TILE_SIZE_BOARD))
            }

    class Dino:
        def __init__(self):
            self.directory = 'dino'
            self.health = 5
            self.damage = 1
            self.delay = 3000
            self.speed = 0.21
            self.frames = {
                'atack': [
                    pygame.transform.scale(load_image(f'Dinoattack{i}.png', 'data/dino/atack').convert_alpha(), (TILE_SIZE_BOARD, TILE_SIZE_BOARD))
                    for i in range(9)
                ],
                'motion': [
                    pygame.transform.scale(load_image(f'Dino{i}.png', 'data/dino/motion').convert_alpha(), (TILE_SIZE_BOARD, TILE_SIZE_BOARD))
                    for i in range(9)
                ],
                'die': [],
                'finish': [
                    pygame.transform.scale(load_image(f'DinoWin{i}.png', 'data/dino/finish').convert_alpha(), (TILE_SIZE_BOARD, TILE_SIZE_BOARD))
                    for i in range(9)
                ],
                'stop': pygame.transform.scale(load_image('dino.png', 'data/dino').convert_alpha(), (TILE_SIZE_BOARD, TILE_SIZE_BOARD))
            }

    class Nail:
        def __init__(self):
            self.directory = 'nail'
            self.health = 10
            self.damage = 2
            self.delay = 4000
            self.speed = 0.18
            self.frames = {
                'atack': [
                    pygame.transform.scale(load_image(f'NailAtk{i + 1}.png', 'data/nail/atack').convert_alpha(), (TILE_SIZE_BOARD, TILE_SIZE_BOARD))
                    for i in range(10)
                ],
                'motion': [
                    pygame.transform.scale(load_image(f'NailWalk{i + 1}.png', 'data/nail/motion').convert_alpha(), (TILE_SIZE_BOARD, TILE_SIZE_BOARD))
                    for i in range(10)
                ],
                'die': [],
                'finish': [
                    pygame.transform.scale(load_image(f'NailWin{i + 1}.png', 'data/nail/finish').convert_alpha(), (TILE_SIZE_BOARD, TILE_SIZE_BOARD))
                    for i in range(10)
                ],
                'stop': pygame.transform.scale(load_image('Nail0.png', 'data/nail').convert_alpha(), (TILE_SIZE_BOARD, TILE_SIZE_BOARD))
            }
