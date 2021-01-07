import pygame
import random
import sys
import os


def load_image(name, colorkey=None):
    fullname = os.path.join('date', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


if __name__ == '__main__':
    pygame.init()
    size = w, h = 750, 800
    screen = pygame.display.set_mode(size)
    running = True
    clock = pygame.time.Clock()
    fps = 60
    all_sprites = pygame.sprite.Group()
    sqr_image = load_image('green_square.png')

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                all_sprites = pygame.sprite.Group()
                bomb = pygame.sprite.Sprite(all_sprites)
                bomb.image = pygame.transform.scale(sqr_image, (75, 75))
                bomb.rect = bomb.image.get_rect()
                bomb.rect.x = random.randint(0, 9) * 75
                bomb.rect.y = 0
                bomb.update()

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(fps)
        pygame.display.flip()
pygame.quit()
