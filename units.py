import pygame
from settings import Settings

LEFT_GAME_BOARD = 541
TOP_GAME_BOARD = 251
TILE_SIZE_BOARD = 150
FPS = 30

all_bullets = pygame.sprite.Group()
all_enemies = pygame.sprite.Group()
all_units = pygame.sprite.Group()


class BaseCharacter(pygame.sprite.Sprite):
    def __init__(self, health, x, y, directory):
        super().__init__()
        self.health = health
        self.x = x
        self.y = y
        self.directory = directory
        self.is_deleted = False

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
        screen.blit(self.image, (x, y))

    def kill(self):
        self.health = 0
        del self

    def __str__(self):
        return self.directory

    def __repr__(self):
        return str(self.directory)

    def __del__(self):
        self.is_deleted = True


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, directory, bullet_speed, bullet_damage, frames):
        super().__init__(all_bullets)
        self.bullet_damage = bullet_damage
        self.bullet_speed = bullet_speed
        self.x = x
        self.y = y
        self.directory = directory
        self.frames = frames
        self.cur_frame = 0
        self.image = self.frames['stop']
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = LEFT_GAME_BOARD + self.x * TILE_SIZE_BOARD, TOP_GAME_BOARD + self.y * TILE_SIZE_BOARD

    def kill(self):
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
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames['motion'][self.cur_frame]
        enemy = pygame.sprite.spritecollideany(self, all_enemies)
        if enemy:
            damage = self.get_bullet_damage()
            enemy.change_health(damage)
            # удаление объектов, если они больше не являются частью игры
            if not enemy.is_alive():
                all_enemies.remove(enemy)
                enemy.kill()
            all_bullets.remove(self)
            self.kill()

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
        self.rect.x, self.rect.y = LEFT_GAME_BOARD + self.x * TILE_SIZE_BOARD, TOP_GAME_BOARD + self.y * TILE_SIZE_BOARD
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
        self.rect.x, self.rect.y = LEFT_GAME_BOARD + self.x * TILE_SIZE_BOARD, TOP_GAME_BOARD + self.y * TILE_SIZE_BOARD

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
        self.rect.x, self.rect.y = LEFT_GAME_BOARD + self.x * TILE_SIZE_BOARD, TOP_GAME_BOARD + self.y * TILE_SIZE_BOARD

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
        self.rect.x, self.rect.y = LEFT_GAME_BOARD + self.x * TILE_SIZE_BOARD, TOP_GAME_BOARD + self.y * TILE_SIZE_BOARD
        self.last_update = pygame.time.get_ticks()
        self.is_walk = True

    def set_mask(self):
        self.mask = pygame.mask.from_surface(self.image)

    def get_damage(self):
        return self.damage

    def update(self):
        current_time = pygame.time.get_ticks()
        unit = pygame.sprite.spritecollideany(self, all_units)
        if unit:
            if self.is_walk:
                self.last_update = current_time - self.delay
            self.is_walk = False
        else:
            self.is_walk = True
        if current_time - self.last_update >= self.delay and not self.is_walk:
            # боевка
            damage = self.get_damage()
            unit.change_health(damage)
            if not unit.is_alive():
                all_units.remove(unit)
                unit.kill()
                unit.is_deleted = True
            self.last_update = current_time
        x, y = self.get_position()
        if self.is_walk:
            x -= self.enemy_speed / FPS
        self.set_position(position=(x, y))
