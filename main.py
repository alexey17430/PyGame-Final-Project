from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QMainWindow, QAction
from PyQt5.QtWidgets import QComboBox, QTableWidget, QTableWidgetItem
from PyQt5 import QtGui
import pygame
import pygame_gui
import random
import sys
import csv
import datetime
import os

sp_squares = list()  # список в который по мере появления будут добавляться объекты кубиков
# формат csv-файла имя игрока\id;количество очков;количество исчезнувших линий; дата; время
map_of_squares = list(list(0 for i in range(10)) for j in range(10))  # карта со всеми элементами
# на экране

NUMBER_OF_SQUARES_WAS_FALLEN = 0
NUMBER_OF_LINES_DELETED = 0
PERSON_COLOR = (255, 0, 0)
SQUARES_COLOR = (0, 255, 0)
PLAYER_NAME = ''
ID_DEFAULT = random.randint(100000, 999999)


# 0 - клетка окна пустая
# 1 - клетка занята кубиком под которым есть другой кубик
# 2 - клетка занята кубиком под которым нет другого кубика
# 3 - клетка занята человечком
# в теле программы нужно сначально проводить изменения координат падающих кубиков(цифра 2),
# только потом создавать новый


class ViewRatingWindow(QMainWindow):
    # класс окна, на котором выводятся тадлицы лидеров

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(800, 600)
        self.setWindowTitle('Таблица лидеров')
        self.font = QtGui.QFont()
        self.font.setPointSize(15)
        self.screen_font = QtGui.QFont()
        self.screen_font.setPointSize(20)
        self.last_id = -1

        self.font = QtGui.QFont()
        self.font.setPointSize(16)

        self.font_big = QtGui.QFont()
        self.font_big.setPointSize(20)
        self.font_big.setBold(True)

        self.table = QTableWidget(self)
        self.table.setFont(self.font)
        self.table.move(50, 100)
        self.table.resize(700, 450)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderItem(0, QTableWidgetItem('Имя игрока'))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem('Заработанные очки'))
        self.table.setHorizontalHeaderItem(2, QTableWidgetItem('Исчезнувшие линии'))
        self.table.setColumnWidth(0, 190)
        self.table.setColumnWidth(1, 250)
        self.table.setColumnWidth(2, 250)
        self.table.setAlternatingRowColors(True)
        #self.table.clicked.connect(self.table_pushed)

        self.btn_sort = QPushButton(self)
        self.btn_sort.move(100, 25)
        self.btn_sort.resize(250, 50)
        self.btn_sort.setFont(self.font)
        self.btn_sort.setText('Показать')
        self.btn_sort.clicked.connect(self.view_pushed)

        self.box_keys = QComboBox(self)
        self.box_keys.setFont(self.font)
        self.box_keys.move(450, 25)
        self.box_keys.resize(250, 50)
        self.box_keys.addItem('В порядке добавления')
        self.box_keys.addItem('По увеличению очков')
        self.box_keys.addItem('По уменьшению очков')
        self.box_keys.addItem('По увеличению исчезнувших линий')
        self.box_keys.addItem('По уменьшению исчезнувших линий')

    def table_pushed(self):
        for elem in self.table.selectedItems():
            self.last_id = str(self.table.item(elem.row(), 0).text())

    def view_pushed(self):
        condition = self.box_keys.currentText()
        rating_file = open(os.path.join('data', 'rating.csv'), 'r')
        reader = list(csv.reader(
            rating_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL))
        self.table.setRowCount(len(reader))
        colvo_pustyh_lines = 0
        if condition == 'В порядке добавления':
            for n in range(len(reader)):
                elem = reader[n]
                if len(elem) > 0:
                    self.table.setItem(n, 0, QTableWidgetItem(elem[0]))
                    self.table.setItem(n, 1, QTableWidgetItem(elem[1]))
                    self.table.setItem(n, 2, QTableWidgetItem(elem[2]))
                else:
                    colvo_pustyh_lines += 1
            self.table.setRowCount(len(reader) - colvo_pustyh_lines)
        elif condition == 'По увеличению очков':
            for i in range(len(reader) - 1):
                for j in range(len(reader) - i - 1):
                    if len(reader[j]) > 0 and len(reader[j + 1]) > 0:
                        if int(reader[j][1]) > int(reader[j + 1][1]):
                            reader[j], reader[j + 1] = reader[j + 1], reader[j]
                    else:
                        continue

            for n in range(len(reader)):
                elem = reader[n]
                if len(elem) > 0:
                    self.table.setItem(n, 0, QTableWidgetItem(elem[0]))
                    self.table.setItem(n, 1, QTableWidgetItem(elem[1]))
                    self.table.setItem(n, 2, QTableWidgetItem(elem[2]))
                else:
                    colvo_pustyh_lines += 1
            self.table.setRowCount(len(reader) - colvo_pustyh_lines)

        elif condition == 'По уменьшению очков':
            for i in range(len(reader) - 1):
                for j in range(len(reader) - i - 1):
                    if len(reader[j]) > 0 and len(reader[j + 1]) > 0:
                        if int(reader[j][1]) < int(reader[j + 1][1]):
                            reader[j], reader[j + 1] = reader[j + 1], reader[j]
                    else:
                        continue
            for n in range(len(reader)):
                elem = reader[n]
                if len(elem) > 0:
                    self.table.setItem(n, 0, QTableWidgetItem(elem[0]))
                    self.table.setItem(n, 1, QTableWidgetItem(elem[1]))
                    self.table.setItem(n, 2, QTableWidgetItem(elem[2]))
                else:
                    colvo_pustyh_lines += 1
            self.table.setRowCount(len(reader) - colvo_pustyh_lines)

        elif condition == 'По увеличению исчезнувших линий':
            for i in range(len(reader) - 1):
                for j in range(len(reader) - i - 1):
                    if len(reader[j]) > 0 and len(reader[j + 1]) > 0:
                        if int(reader[j][2]) > int(reader[j + 1][2]):
                            reader[j], reader[j + 1] = reader[j + 1], reader[j]
                    else:
                        continue

            for n in range(len(reader)):
                elem = reader[n]
                if len(elem) > 0:
                    self.table.setItem(n, 0, QTableWidgetItem(elem[0]))
                    self.table.setItem(n, 1, QTableWidgetItem(elem[1]))
                    self.table.setItem(n, 2, QTableWidgetItem(elem[2]))
                else:
                    colvo_pustyh_lines += 1
            self.table.setRowCount(len(reader) - colvo_pustyh_lines)

        elif condition == 'По уменьшению исчезнувших линий':
            for i in range(len(reader) - 1):
                for j in range(len(reader) - i - 1):
                    if len(reader[j]) > 0 and len(reader[j + 1]) > 0:
                        if int(reader[j][2]) < int(reader[j + 1][2]):
                            reader[j], reader[j + 1] = reader[j + 1], reader[j]
                    else:
                        continue

            for n in range(len(reader)):
                elem = reader[n]
                if len(elem) > 0:
                    self.table.setItem(n, 0, QTableWidgetItem(elem[0]))
                    self.table.setItem(n, 1, QTableWidgetItem(elem[1]))
                    self.table.setItem(n, 2, QTableWidgetItem(elem[2]))
                else:
                    colvo_pustyh_lines += 1
            self.table.setRowCount(len(reader) - colvo_pustyh_lines)


class AboutWindow(QWidget):
    def __init__(self):
        super(AboutWindow, self).__init__()
        self.setGeometry(700, 400, 550, 200)
        self.setWindowTitle('Справка')
        self.initUI()

    def initUI(self):
        self.font = QtGui.QFont()
        self.font.setPointSize(15)

        self.lbl = QLabel(self)
        self.lbl.move(25, 25)
        self.lbl.resize(500, 150)
        self.lbl.setFont(self.font)
        self.lbl.setText(f'Количество заработанных очков - это число кубиков,\n'
                         f'которые выпали за всё время вашей игры.\n\n'
                         f'Количество исчезнувших линий кубиков - это число\n'
                         f'линий из кубиков, которые исчезли в ходе игры,\n'
                         f'если вся нижняя полоса была заполнена.')


class EndGameWindow(QMainWindow):
    # класс окна, на котором выводится информация после игры

    def __init__(self):
        super().__init__()
        self.initUI()

    def about_show(self):
        self.about_window.show()

    def initUI(self):
        self.resize(500, 625)
        self.setWindowTitle('Игра окончена')
        self.font = QtGui.QFont()
        self.font.setPointSize(15)
        self.screen_font = QtGui.QFont()
        self.screen_font.setPointSize(20)

        self.about_action = QAction(self)
        self.about_action.triggered.connect(self.about_show)
        self.about_action.setText('Справка')
        self.menuBar().addAction(self.about_action)
        self.about_window = AboutWindow()

        self.lbl = QLabel(self)
        self.lbl.move(25, 25 + 25)
        self.lbl.resize(450, 75)
        self.lbl.setFont(self.screen_font)
        self.lbl.setText('Ваши результаты\nпо окончанию игры:')

        global NUMBER_OF_SQUARES_WAS_FALLEN
        self.lbl1 = QLabel(self)
        self.lbl1.move(25, 125 + 50)
        self.lbl1.resize(450, 75)
        self.lbl1.setFont(self.font)
        self.lbl1.setText(f'Количество заработанных очков: {NUMBER_OF_SQUARES_WAS_FALLEN}')

        global NUMBER_OF_LINES_DELETED
        self.lbl2 = QLabel(self)
        self.lbl2.move(25, 225 + 50)
        self.lbl2.resize(450, 75)
        self.lbl2.setFont(self.font)
        self.lbl2.setText(f'Количество исчезнувших линий кубиков: {NUMBER_OF_LINES_DELETED}')

        global PLAYER_NAME
        self.lbl3 = QLabel(self)
        self.lbl3.move(25, 225 + 50 + 100)
        self.lbl3.resize(450, 75)
        self.lbl3.setFont(self.font)
        if PLAYER_NAME == '':
            global ID_DEFAULT
            self.lbl3.setText('Имя игрока: не выбрано')
            with open(os.path.join('data', 'rating.csv'), 'a', encoding="utf8") as csvfile:
                writer = csv.writer(
                    csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                date, time = str(datetime.datetime.now()).split()
                writer.writerow([str(random.randint(100000, 999999)),
                                 str(NUMBER_OF_SQUARES_WAS_FALLEN),
                                 str(NUMBER_OF_LINES_DELETED),
                                 str(date), str(time)])
        else:
            self.lbl3.setText(f'Имя игрока: {PLAYER_NAME}')
            with open(os.path.join('data', 'rating.csv'), 'a', encoding="utf8") as csvfile:
                writer = csv.writer(
                    csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                date, time = str(datetime.datetime.now()).split()
                writer.writerow([str(PLAYER_NAME),
                                 str(NUMBER_OF_SQUARES_WAS_FALLEN),
                                 str(NUMBER_OF_LINES_DELETED),
                                 str(date), str(time)])

        self.btn = QPushButton(self)
        self.btn.move(100, 475)
        self.btn.resize(300, 100)
        self.btn.setFont(self.screen_font)
        self.btn.setText('Вернуться на\n'
                         'главный экран')
        self.btn.clicked.connect(self.btn_pushed)

    def btn_pushed(self):
        global start_one_more_time
        start_one_more_time = True
        self.close()


class Square:
    # класс описывающий действия кубиков
    def __init__(self):
        self.TILE_SIZE = 75
        self.pos_x = random.randint(0, 9)
        self.pos_y = 0
        self.is_flying = True
        self.should_fall_out = False
        if map_of_squares[self.pos_y + 1][self.pos_x] == 1:
            map_of_squares[self.pos_y][self.pos_x] = 1
        else:
            map_of_squares[self.pos_y][self.pos_x] = 2

    # метод в котором описана физика падения кубиков
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

        if self.should_fall_out:
            self.fall_out()

    # возвращает состояние кубика: летит или нет
    def get_sqr_process(self):
        if self.should_fall_out:
            self.fall_out()
        return self.is_flying

    # рисование кубика
    def drawing(self):
        if self.should_fall_out:
            self.fall_out()
        pygame.draw.rect(screen, SQUARES_COLOR, (self.pos_x * 75 + 2, self.pos_y * 75 + 2,
                                                 self.TILE_SIZE - 2, self.TILE_SIZE - 2))

    # возвращает координаты кубика
    def get_coords(self):
        if self.pos_y + 1 <= 9 and map_of_squares[self.pos_y + 1][self.pos_x] == 0:
            self.should_fall_out = True
        if self.should_fall_out:
            self.fall_out()
        return self.pos_x, self.pos_y

    # принудительное падение после каких-либо перемещений
    def fall_out(self):
        if self.pos_y + 1 <= 9 and map_of_squares[self.pos_y + 1][self.pos_x] == 0 and \
                map_of_squares[self.pos_y][self.pos_x] == 1:
            self.sqr_move('y', 1)  # cпускаемся вниз

    # изменяет координаты кубика
    def sqr_move(self, destination, delta):
        if destination == 'x':
            pygame.draw.rect(screen, (0, 0, 0), (self.pos_x * 75 + 2, self.pos_y * 75 + 2,
                                                 self.TILE_SIZE - 2, self.TILE_SIZE - 2))
            map_of_squares[self.pos_y][self.pos_x] = 0
            self.pos_x += delta
            map_of_squares[self.pos_y][self.pos_x] = 1
            if self.pos_y + 1 <= 9 and map_of_squares[self.pos_y + 1][self.pos_x] == 0:
                self.should_fall_out = True
        if destination == 'y':
            pygame.draw.rect(screen, (0, 0, 0), (self.pos_x * 75 + 2, self.pos_y * 75 + 2,
                                                 self.TILE_SIZE - 2, self.TILE_SIZE - 2))
            map_of_squares[self.pos_y][self.pos_x] = 0
            self.pos_y += delta
            map_of_squares[self.pos_y][self.pos_x] = 1
            if self.pos_y + 1 <= 9 and map_of_squares[self.pos_y + 1][self.pos_x] == 0:
                self.should_fall_out = True
        if self.should_fall_out:
            self.fall_out()


class Person:
    # класс описывающий действия персонажа
    def __init__(self):
        self.TILE_SIZE = 75
        self.pos_x = 4
        self.pos_y = 9
        map_of_squares[self.pos_y][self.pos_x] = 3
        self.flag_proverka_down = True

    # возвращает координаты персонажа
    def get_coords(self):
        return self.pos_x, self.pos_y

    # передвижение персонажа
    def move(self, button):
        pygame.draw.rect(screen, (0, 0, 0), (self.pos_x * 75, self.pos_y * 75, 75, 75))

        # изменение положения на одну клетку влево
        if button == 92 and self.pos_x != 0 and map_of_squares[self.pos_y][self.pos_x - 1] == 0:
            map_of_squares[self.pos_y][self.pos_x] = 0
            self.pos_x -= 1
            map_of_squares[self.pos_y][self.pos_x] = 3

        # изменение положения на одну клетку влево и вверх
        elif button == 95 and self.pos_x != 0 and self.pos_y != 0 and \
                map_of_squares[self.pos_y - 1][self.pos_x - 1] == 0:
            map_of_squares[self.pos_y][self.pos_x] = 0
            self.pos_x -= 1
            self.pos_y -= 1
            map_of_squares[self.pos_y][self.pos_x] = 3

        # изменение положения на одну клетку вправо и вверх
        elif button == 97 and self.pos_x != 9 and self.pos_y != 0 and \
                map_of_squares[self.pos_y - 1][self.pos_x + 1] == 0:
            map_of_squares[self.pos_y][self.pos_x] = 0
            self.pos_x += 1
            self.pos_y -= 1
            map_of_squares[self.pos_y][self.pos_x] = 3

        # изменение положения на одну клетку вправо
        elif button == 94 and self.pos_x != 9 and \
                map_of_squares[self.pos_y][self.pos_x + 1] == 0:
            map_of_squares[self.pos_y][self.pos_x] = 0
            self.pos_x += 1
            map_of_squares[self.pos_y][self.pos_x] = 3

        # персонаж опускается вниз, если снизу пусто
        elif button == 93 and self.pos_y != 9 and map_of_squares[self.pos_y + 1][self.pos_x] == 0:
            map_of_squares[self.pos_y][self.pos_x] = 0
            self.pos_y += 1
            map_of_squares[self.pos_y][self.pos_x] = 3

    # рисование персонажа
    def draw(self):
        # левая нога персонажа
        pygame.draw.line(screen, PERSON_COLOR,
                         (self.pos_x * self.TILE_SIZE + 20,
                          (self.pos_y + 1) * self.TILE_SIZE - 1),
                         (self.pos_x * self.TILE_SIZE + (self.TILE_SIZE - 5) // 2,
                          self.pos_y * self.TILE_SIZE + (2 * self.TILE_SIZE // 3)), width=5)

        # правая нога персонажа
        pygame.draw.line(screen, PERSON_COLOR,
                         ((self.pos_x + 1) * self.TILE_SIZE - 20,
                          (self.pos_y + 1) * self.TILE_SIZE - 1),
                         (self.pos_x * self.TILE_SIZE + (self.TILE_SIZE - 5) // 2,
                          self.pos_y * self.TILE_SIZE + (2 * self.TILE_SIZE // 3)), width=5)

        # тело персонажа
        pygame.draw.line(screen, PERSON_COLOR,
                         (self.pos_x * self.TILE_SIZE + (self.TILE_SIZE - 5) // 2,
                          self.pos_y * self.TILE_SIZE + (2 * self.TILE_SIZE // 3)),
                         (self.pos_x * self.TILE_SIZE + (self.TILE_SIZE - 5) // 2,
                          self.pos_y * self.TILE_SIZE + (1 * self.TILE_SIZE // 3)), width=5)

        # голова персонажа
        pygame.draw.circle(screen, PERSON_COLOR,
                           (self.pos_x * self.TILE_SIZE + (self.TILE_SIZE - 5) // 2,
                            self.pos_y * self.TILE_SIZE + (1 * self.TILE_SIZE // 3) - (self.TILE_SIZE // 6)),
                           (self.TILE_SIZE // 6))

        # левая рука персонажа
        pygame.draw.line(screen, PERSON_COLOR,
                         (self.pos_x * self.TILE_SIZE + (self.TILE_SIZE - 5) // 2,
                          self.pos_y * self.TILE_SIZE + (2 * self.TILE_SIZE // 3) - (self.TILE_SIZE // 6)),
                         (self.pos_x * self.TILE_SIZE + (self.TILE_SIZE - 5) // 2 - 20,
                          self.pos_y * self.TILE_SIZE + (2 * self.TILE_SIZE // 3) - (self.TILE_SIZE // 6)), width=5)

        # правая рука персонажа
        pygame.draw.line(screen, PERSON_COLOR,
                         (self.pos_x * self.TILE_SIZE + (self.TILE_SIZE - 5) // 2,
                          self.pos_y * self.TILE_SIZE + (2 * self.TILE_SIZE // 3) - (self.TILE_SIZE // 6)),
                         (self.pos_x * self.TILE_SIZE + (self.TILE_SIZE - 5) // 2 + 20,
                          self.pos_y * self.TILE_SIZE + (2 * self.TILE_SIZE // 3) - (self.TILE_SIZE // 6)), width=5)


def main():
    # главная функция, в которой находится тело игры
    running = True
    clock = pygame.time.Clock()
    fps = 5
    ex_person = Person()
    ex_person.draw()

    # игровой цикл
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # нажатие цифр 4, 7, 8, 9, 6 приводят к передвижению человечка
            if event.type == pygame.KEYDOWN:
                # нажата одна из кнопок отвечающих за перемещение персонажа
                if event.scancode in [92, 95, 96, 97, 94]:
                    ex_per_x, ex_per_y = ex_person.get_coords()
                    # персонаж двигает кубик слева и двигается сам влево
                    if event.scancode == 92 and ex_per_x - 2 >= 0 and ex_per_y - 1 >= 0 and \
                            map_of_squares[ex_per_y][ex_per_x - 1] == 1 and \
                            map_of_squares[ex_per_y][ex_per_x - 2] == 0 and \
                            map_of_squares[ex_per_y - 1][ex_per_x - 1] == 0:
                        for elem in sp_squares:
                            if list(elem.get_coords()) == [ex_per_x - 1, ex_per_y]:
                                elem.sqr_move('x', -1)
                        ex_person.move(event.scancode)
                    # персонаж двигает ккубик справа и двигается сам вправо
                    elif event.scancode == 94 and ex_per_x + 2 <= 9 and ex_per_y - 1 >= 0 and \
                            map_of_squares[ex_per_y][ex_per_x + 1] == 1 and \
                            map_of_squares[ex_per_y][ex_per_x + 2] == 0 and \
                            map_of_squares[ex_per_y - 1][ex_per_x + 1] == 0:
                        for elem in sp_squares:
                            if list(elem.get_coords()) == [ex_per_x + 1, ex_per_y]:
                                elem.sqr_move('x', 1)
                        ex_person.move(event.scancode)
                    # персонаж двигает кубик слева сверху и двигается сам на его место
                    elif event.scancode == 95 and map_of_squares[ex_per_y][ex_per_x - 1] == 1 and\
                            map_of_squares[ex_per_y - 1][ex_per_x - 1] == 1 and\
                            map_of_squares[ex_per_y - 2][ex_per_x - 1] == 0 and\
                            map_of_squares[ex_per_y - 1][ex_per_x - 2] == 0 and \
                            ex_per_x >= 2:
                        for elem in sp_squares:
                            if list(elem.get_coords()) == [ex_per_x - 1, ex_per_y - 1]:
                                elem.sqr_move('x', -1)
                        ex_person.move(event.scancode)
                    # персонаж двигает кубик справа сверху и двигается сам на его место
                    elif event.scancode == 97 and ex_per_x <= 7 and\
                            map_of_squares[ex_per_y][ex_per_x + 1] == 1 and\
                            map_of_squares[ex_per_y - 1][ex_per_x + 1] == 1 and\
                            map_of_squares[ex_per_y - 2][ex_per_x + 1] == 0 and\
                            map_of_squares[ex_per_y - 1][ex_per_x + 2] == 0:
                        for elem in sp_squares:
                            if list(elem.get_coords()) == [ex_per_x + 1, ex_per_y - 1]:
                                elem.sqr_move('x', 1)
                        ex_person.move(event.scancode)
                    else:
                        ex_person.move(event.scancode)

        # если под персонажем пусто, то он падает
        ex_per_x, ex_per_y = ex_person.get_coords()
        if ex_per_y != 9 and map_of_squares[ex_per_y + 1][ex_per_x] == 0:
            ex_person.move(93)

        # на окошке появляется соответствующая информация если на человечка упал кирпич, а каски на голове не было
        if ex_per_y != 0 and (map_of_squares[ex_per_y - 1][ex_per_x] == 1 or
                              map_of_squares[ex_per_y - 1][ex_per_x] == 2):
            # появляется окошко с информацией об окончании игры
            app1 = QApplication(sys.argv)
            ex1 = EndGameWindow()
            ex1.show()
            app1.exec()
            return None

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
            global NUMBER_OF_SQUARES_WAS_FALLEN
            NUMBER_OF_SQUARES_WAS_FALLEN += 1
        else:
            # прорисовка всех кубиков
            for elem in sp_squares:
                elem.falling()
                elem.drawing()

        # удаление нижнего ряда, если все клетки в нём заняты кубиками
        if 0 not in map_of_squares[9] and 3 not in map_of_squares[9]:
            global NUMBER_OF_LINES_DELETED
            NUMBER_OF_LINES_DELETED += 1
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
                if elem.pos_y + 1 <= 9:
                    map_of_squares[elem.pos_y][elem.pos_x] = 0
                    elem.pos_y += 1
                    map_of_squares[elem.pos_y][elem.pos_x] = 1

            screen.fill((0, 0, 0))
            for elem in sp_squares:
                elem.drawing()

        ex_person.draw()  # рисование персонажа в конце каждого хода

        clock.tick(fps)
        pygame.display.flip()


def start_window():
    # функция в которой находится стартовое окно
    manager = pygame_gui.UIManager((750, 750))
    clock = pygame.time.Clock()
    run = True
    flag_game_start_pushed = False

    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render("Выберите цвет персонажа и кубиков", True, (100, 255, 100))
    text_x = w // 2 - text.get_width() // 2
    text_y = h // 2 - text.get_height() // 2 - 250
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)

    # кнопка начала игры
    start_game_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((275, 300 - 75), (200, 50)),
        text='Старт',
        manager=manager
    )

    # выпадающий список для выбора цвета персонажа
    person_color = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
        options_list=['Красный', 'Зелёный', 'Cиний'],
        starting_option='Красный',
        relative_rect=pygame.Rect((275, 400 - 75), (200, 50)),
        manager=manager
    )

    # выпадающий список для выбора цвета кубиков
    squares_color = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
        options_list=['Красный', 'Зелёный', 'Cиний'],
        starting_option='Зелёный',
        relative_rect=pygame.Rect((275, 500 - 75), (200, 50)),
        manager=manager
    )

    # строка, в которую необходимо ввести своё имя перед началом игры
    line_with_name = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((275, 600 - 75), (200, 50)),
        manager=manager
    )

    # кнопка просмотра таблицы лидеров
    view_rating_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((275, 680 - 75), (200, 50)),
        text='Просмотр тадлицы лидеров',
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
                        return False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_element == line_with_name:
                    global PLAYER_NAME
                    PLAYER_NAME = event.text

                if event.user_type == pygame_gui.UI_BUTTON_PRESSED and\
                        event.ui_element == view_rating_button:
                    app2 = QApplication(sys.argv)
                    ex2 = ViewRatingWindow()
                    ex2.show()
                    app2.exec()

                # изменение цвета персонажа
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED and\
                        event.ui_element == person_color:
                    global PERSON_COLOR
                    if event.text == 'Красный':
                        PERSON_COLOR = (255, 0, 0)
                    if event.text == 'Зелёный':
                        PERSON_COLOR = (0, 255, 0)
                    if event.text == 'Cиний':
                        PERSON_COLOR = (0, 0, 255)

                # изменение цвета кубиков
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED and\
                        event.ui_element == squares_color:
                    global SQUARES_COLOR
                    if event.text == 'Красный':
                        SQUARES_COLOR = (255, 0, 0)
                    if event.text == 'Зелёный':
                        SQUARES_COLOR = (0, 255, 0)
                    if event.text == 'Cиний':
                        SQUARES_COLOR = (0, 0, 255)

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
                        text_y = h // 2 - text.get_height() // 2 - 250
                        text_w = text.get_width()
                        text_h = text.get_height()
                        screen.blit(text, (text_x, text_y))
                        pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                                               text_w + 20, text_h + 20), 1)

                if event.user_type == pygame_gui.UI_BUTTON_ON_UNHOVERED and not flag_game_start_pushed:
                    if event.ui_element == start_game_button:
                        screen.fill((0, 0, 0))
                        font = pygame.font.Font(None, 50)
                        text = font.render("Выберите цвет персонажа и кубиков", True, (100, 255, 100))
                        text_x = w // 2 - text.get_width() // 2
                        text_y = h // 2 - text.get_height() // 2 - 250
                        text_w = text.get_width()
                        text_h = text.get_height()
                        screen.blit(text, (text_x, text_y))
                        pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                                               text_w + 20, text_h + 20), 1)

            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()
    return False


if __name__ == '__main__':
    pygame.init()
    size = w, h = 750, 750
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Сортировщик кирпичей')
    start_one_more_time = False

    while True:
        screen.fill((0, 0, 0))
        flag = start_window()
        if flag:
            screen.fill((0, 0, 0))
            NUMBER_OF_LINES_DELETED = 0
            NUMBER_OF_SQUARES_WAS_FALLEN = 0
            sp_squares = list()  # список в который по мере появления будут добавляться объекты кубиков
            map_of_squares = list(list(0 for i in range(10)) for j in range(10))  # карта со всеми элементами на экране
            main()
        if not start_one_more_time:
            break
        start_one_more_time = False

    pygame.quit()
