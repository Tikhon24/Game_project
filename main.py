import pygame

SIZE = WIDTH, HEIGHT = (1600, 900)


def main():
    # инициализация игры
    pygame.init()

    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Игра')

    running = True
    # игровой цикл
    while running:
        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

        screen.fill((0, 0, 0))
        pygame.display.flip()


if __name__ == '__main__':
    main()
