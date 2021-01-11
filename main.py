from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLineEdit
from PyQt5 import QtGui
import pygame
import pygame_gui
import random
import sys
import os
import time


dict_squares = dict()  # словарь в который по мере появления будут добавляться объекты кубиков

map_of_squares = list(list(0 for i in range(10)) for j in range(10))  # карта со всеми элементами на экране
# 0 - клетка окна пустая
# 1 - клетка занята кубиком под которым есть другой кубик
# 2 - клетка занята кубиком под которым нет другого кубика
# в теле программы нужно сначально проводить изменения координат падающих кубиков(цифра 2), только потом создавать новый


class Example(QWidget):
    # класс окна, на котором выводится таблица рекордов

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(500, 500)
        self.setWindowTitle('Таблица рекордов')
        font = QtGui.QFont()
        font.setPointSize(16)
        screen_font = QtGui.QFont()
        screen_font.setPointSize(20)

        self.btn = QPushButton(self)
        self.btn.move(150, 200)
        self.btn.resize(200, 100)
        self.btn.setText('Показать\nтаблицу\nрекордов')
        self.btn.setFont(font)


# функция для загрузки изображения
def load_image(name, colorkey=None):
    # имя картинки, находящейся в папке data
    fullname = os.path.join('date', name)
    # программа прекращает выполнение если указанной картинки нет
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    # клетчатый фон становится прозрачным, если это картинка png с прозрачностью
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Square:
    #  sqr_image = load_image('green_square.png')

    def __init__(self):
        self.pos_x = random.randint(0, 9)
        self.pos_y = 0
        self.is_lying = False
        if map_of_squares[self.pos_y + 1][self.pos_x] == 1:
            map_of_squares[self.pos_y][self.pos_x] = 1
        else:
            map_of_squares[self.pos_y][self.pos_x] = 2

    # проверка на поражение игрока
    def check_for_lose(self):
        flag = False
        for elem in map_of_squares[0]:
            if not elem == 0 or not elem == 2:
                flag = True
                break
        return flag

    def falling(self):
        if map_of_squares[self.pos_y + 1][self.pos_x] == 1:
            self.is_lying = True

        if not self.is_lying:
            map_of_squares[self.pos_y][self.pos_x] = 0
            self.pos_y += 1
            if map_of_squares[self.pos_y + 1][self.pos_x] == 1:
                map_of_squares[self.pos_y][self.pos_x] = 1
            else:
                map_of_squares[self.pos_y][self.pos_x] = 2


def main():
    # главная функция, в которой находится тело программы игры
    running = True
    clock = pygame.time.Clock()
    fps = 60
    all_sprites = pygame.sprite.Group()
    sqr_image = load_image('green_square.png')
    person_image = load_image('главный персонаж.png')
    person_coords = [0, 675]

    # человечек рисуется на холсте сразу же после вызова функции main
    person = pygame.sprite.Sprite(all_sprites)
    person.image = pygame.transform.scale(person_image, (75, 75))
    person.rect = person.image.get_rect()
    person.rect.x = person_coords[0]
    person.rect.y = person_coords[1]
    person.update()

    flag_game_started_writing = True

    # игровой цикл
    while running:
        if flag_game_started_writing:
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                flag_game_started_writing = False
            # нажатие стрелочек приводят к передвижению человечка
            if event.type == pygame.KEYDOWN and event.scancode in [79, 80, 82, 19]:
                flag_game_started_writing = False
                all_sprites = pygame.sprite.Group()
                square = pygame.sprite.Sprite(all_sprites)
                square.image = pygame.transform.scale(sqr_image, (75, 75))
                square.rect = square.image.get_rect()
                square.rect.x = 0
                square.rect.y = 0
                square.update()

                # нажата кнопка P - постановка на паузу
                if event.scancode == 19:
                    pass

                # перемещение направо
                if event.scancode == 79:
                    person = pygame.sprite.Sprite(all_sprites)
                    person.image = pygame.transform.scale(person_image, (75, 75))
                    person.rect = person.image.get_rect()
                    person_coords[0] += 75
                    person.rect.x = person_coords[0]
                    person.rect.y = person_coords[1]
                    person.update()
                # перемещение налево
                elif event.scancode == 80:
                    person = pygame.sprite.Sprite(all_sprites)
                    person.image = pygame.transform.scale(person_image, (75, 75))
                    person.rect = person.image.get_rect()
                    person_coords[0] -= 75
                    person.rect.x = person_coords[0]
                    person.rect.y = person_coords[1]
                    person.update()
                # прыжок персонажа
                elif event.scancode == 82:
                    person = pygame.sprite.Sprite(all_sprites)
                    person.image = pygame.transform.scale(person_image, (75, 75))
                    person.rect = person.image.get_rect()
                    person_coords[1] -= 75
                    person.rect.x = person_coords[0]
                    person.rect.y = person_coords[1]
                    person.update()

        if not flag_game_started_writing:
            screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(fps)
        pygame.display.flip()


def start_window():
    # функция в которой находится стартовое окно
    manager = pygame_gui.UIManager((750, 750))
    clock = pygame.time.Clock()
    run = True
    flag_game_start_pushed = False

    # кнопка начала игры
    start_game_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((275, 250), (200, 50)),
        text='Старт',
        manager=manager
    )

    # открытие окна с рейтингами игроков
    results_table_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((275, 350), (200, 50)),
        text='Таблица результатов',
        manager=manager
    )

    # поле для ввода имени игрока, который собирается играть
    line_player_name = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((275, 450), (200, 50)),
        manager=manager
    )

    while run:
        time_delta = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # окно, которое появляется при попытке закрыть стартовое окно
                confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((250, 200), (300, 200)),
                    manager=manager,
                    window_title='Подтверждение',
                    action_long_desc='Вы уверены, что хотите выйти?',
                    action_short_name='OK',
                    blocking=True
                )
                # если на всплывающем окне нажата кнопка OK, закрывается стартовое окно
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    if event.ui_element == confirmation_dialog:
                        run = False

            if event.type == pygame.USEREVENT:
                # при нажатии на кнопку "Таблица результатов" появляется PyQt окно с таблицой рекордов
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == results_table_button:
                        app = QApplication(sys.argv)
                        ex = Example()
                        ex.show()
                        app.exec()

                # при нажатии на кнопку "Начало игры" появляется надпись "Игра начинается"
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_game_button:
                        return True
                        # можно запускать окно игры

                # при наведении на кнопку "Начало игры" появляется надпись "Игра готовится к запуску..."
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
    return False


if __name__ == '__main__':
    pygame.init()
    size = w, h = 750, 750
    screen = pygame.display.set_mode(size)

    flag = start_window()
    if flag:
        main()
    pygame.quit()
