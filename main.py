from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLineEdit
from PyQt5 import QtGui
import pygame
import pygame_gui
import random
import sys
import os
import time


sp_squares = list()  # словарь в который по мере появления будут добавляться объекты кубиков

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
    def __init__(self):
        self.TILE_SIZE = 75
        self.pos_x = random.randint(0, 9)
        self.pos_y = 0
        self.is_flying = True
        if map_of_squares[self.pos_y + 1][self.pos_x] == 1:
            map_of_squares[self.pos_y][self.pos_x] = 1
        else:
            map_of_squares[self.pos_y][self.pos_x] = 2

    def falling(self):
        if self.pos_y == 9 or map_of_squares[self.pos_y + 1][self.pos_x] == 1:
            self.is_flying = False

        if self.is_flying:
            pygame.draw.rect(screen, (0, 0, 0), (self.pos_x * 75 + 2, self.pos_y * 75 + 2,
                                                   self.TILE_SIZE - 2, self.TILE_SIZE - 2))
            map_of_squares[self.pos_y][self.pos_x] = 0
            self.pos_y += 1
            if self.pos_y == 9:
                map_of_squares[self.pos_y][self.pos_x] = 1
            elif map_of_squares[self.pos_y + 1][self.pos_x] == 1:
                map_of_squares[self.pos_y][self.pos_x] = 1
            else:
                map_of_squares[self.pos_y][self.pos_x] = 2

    def get_sqr_process(self):
        return self.is_flying

    def drawing(self):
        pygame.draw.rect(screen, (0, 255, 0), (self.pos_x * 75 + 2, self.pos_y * 75 + 2,
                                               self.TILE_SIZE - 2, self.TILE_SIZE - 2))

    def get_coords(self):
        return self.pos_x, self.pos_y

    def set_coords(self, x, y):
        if x != self.pos_x or y != self.pos_y:
            pygame.draw.rect(screen, (0, 0, 0), (self.pos_x * 75 + 2, self.pos_y * 75 + 2,
                                                   self.TILE_SIZE - 2, self.TILE_SIZE - 2))
            map_of_squares[self.pos_y][self.pos_x] = 0
        self.pos_x = x
        self.pos_y = y
        map_of_squares[self.pos_y][self.pos_x] = 1


def main():
    # главная функция, в которой находится тело игры
    running = True
    clock = pygame.time.Clock()
    fps = 5

    # игровой цикл
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # нажатие стрелочек приводят к передвижению человечка
            if event.type == pygame.KEYDOWN and event.scancode in [79, 80, 82, 19]:

                # нажата кнопка P - постановка на паузу
                if event.scancode == 19:
                    pass

                # перемещение направо
                if event.scancode == 79:
                    pass

                # перемещение налево
                elif event.scancode == 80:
                    pass

                # прыжок персонажа
                elif event.scancode == 82:
                    pass

        # создание нового падающего квадрата
        flag_there_is_not_flying = True  # нет летящих кубов - True, есть летящие кубы - False
        for value in sp_squares:
            if value.get_sqr_process():
                flag_there_is_not_flying = False
        if flag_there_is_not_flying:
            # создание нового кубика
            sqr_example = Square()
            sqr_example.drawing()
            sp_squares.append(sqr_example)
        else:
            # прорисовка всех кубиков
            for elem in sp_squares:
                elem.falling()
                elem.drawing()

        # удаление нижнего ряда, если все клетки в нём заняты кубиками
        if 0 not in map_of_squares[9]:
            for i in range(10):
                j = 0
                for j in range(len(sp_squares)):
                    elem = sp_squares[j]
                    if elem.get_coords()[1] == 9:
                        break
                del sp_squares[j]
            for i in range(10):
                map_of_squares[9][i] = 0
            for elem in sp_squares:
                map_of_squares[elem.pos_y][elem.pos_x] = 0
                elem.pos_y += 1
                map_of_squares[elem.pos_y][elem.pos_x] = 1

            screen.fill((0, 0, 0))
            for elem in sp_squares:
                elem.drawing()

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

    #flag = start_window()
    #if flag:
        #main()
    main()
    pygame.quit()
