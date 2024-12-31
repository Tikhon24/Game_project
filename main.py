import pygame


def main():
    pygame.init()

    size = width, height = (600, 600)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Игра')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

        screen.fill((0, 0, 0))
        pygame.display.flip()


if __name__ == '__main__':
    main()
