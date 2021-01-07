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
    size = w, h = 750, 750
    screen = pygame.display.set_mode(size)
    running = True
    clock = pygame.time.Clock()
    fps = 60
    all_sprites = pygame.sprite.Group()
    sqr_image = load_image('green_square.png')
    person_image = load_image('главный персонаж.png')
    person_coords = [0, 675]

    person = pygame.sprite.Sprite(all_sprites)
    person.image = pygame.transform.scale(person_image, (75, 75))
    person.rect = person.image.get_rect()
    person.rect.x = person_coords[0]
    person.rect.y = person_coords[1]
    person.update()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                all_sprites = pygame.sprite.Group()
                square = pygame.sprite.Sprite(all_sprites)
                square.image = pygame.transform.scale(sqr_image, (75, 75))
                square.rect = square.image.get_rect()
                square.rect.x = random.randint(0, 9) * 75
                square.rect.y = 0
                square.update()

                if event.scancode == 79:
                    person = pygame.sprite.Sprite(all_sprites)
                    person.image = pygame.transform.scale(person_image, (75, 75))
                    person.rect = person.image.get_rect()
                    person_coords[0] += 75
                    person.rect.x = person_coords[0]
                    person.rect.y = person_coords[1]
                    person.update()
                elif event.scancode == 80:
                    person = pygame.sprite.Sprite(all_sprites)
                    person.image = pygame.transform.scale(person_image, (75, 75))
                    person.rect = person.image.get_rect()
                    person_coords[0] -= 75
                    person.rect.x = person_coords[0]
                    person.rect.y = person_coords[1]
                    person.update()
                elif event.scancode == 82:
                    person = pygame.sprite.Sprite(all_sprites)
                    person.image = pygame.transform.scale(person_image, (75, 75))
                    person.rect = person.image.get_rect()
                    person_coords[1] -= 75
                    person.rect.x = person_coords[0]
                    person.rect.y = person_coords[1]
                    person.update()

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(fps)
        pygame.display.flip()
pygame.quit()
