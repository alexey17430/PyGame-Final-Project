import pygame
import pygame_gui
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


def main():
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
                square.rect.x = 0
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


def start_window():
    manager = pygame_gui.UIManager((750, 750))
    clock = pygame.time.Clock()
    run = True
    flag_game_start_pushed = False

    start_game_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((275, 250), (200, 50)),
        text='Старт',
        manager=manager
    )

    results_table_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((275, 350), (200, 50)),
        text='Таблица результатов',
        manager=manager
    )

    line_player_name = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((275, 450), (200, 50)),
        manager=manager
    )

    while run:
        time_delta = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((250, 200), (300, 200)),
                    manager=manager,
                    window_title='Подтверждение',
                    action_long_desc='Вы уверены, что хотите выйти?',
                    action_short_name='OK',
                    blocking=True
                )
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    if event.ui_element == confirmation_dialog:
                        run = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_game_button:
                        flag_game_start_pushed = True
                        screen.fill((0, 0, 0))
                        font = pygame.font.Font(None, 50)
                        text = font.render("Игра начинается", True, (100, 255, 100))
                        text_x = w // 2 - text.get_width() // 2
                        text_y = h // 2 - text.get_height() // 2 - 200
                        text_w = text.get_width()
                        text_h = text.get_height()
                        screen.blit(text, (text_x, text_y))
                        pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                                               text_w + 20, text_h + 20), 1)

                if event.user_type == pygame_gui.UI_BUTTON_ON_HOVERED and not flag_game_start_pushed:
                    if event.ui_element == start_game_button:
                        screen.fill((0, 0, 0))
                        font = pygame.font.Font(None, 50)
                        text = font.render("Игра готовится к запуску...", True, (100, 255, 100))
                        text_x = w // 2 - text.get_width() // 2
                        text_y = h // 2 - text.get_height() // 2 - 200
                        text_w = text.get_width()
                        text_h = text.get_height()
                        screen.blit(text, (text_x, text_y))
                        pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                                               text_w + 20, text_h + 20), 1)

                if event.user_type == pygame_gui.UI_BUTTON_ON_UNHOVERED and not flag_game_start_pushed:
                    if event.ui_element == start_game_button:
                        screen.fill((0, 0, 0))

            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    size = w, h = 750, 750
    screen = pygame.display.set_mode(size)
    start_window()
    #main()
    pygame.quit()
