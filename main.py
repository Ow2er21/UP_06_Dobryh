import sys
import os
import time
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QVBoxLayout, QLabel, QSizePolicy, \
    QHBoxLayout, QStackedWidget

class ResultWindow(QWidget):
    def __init__(self, levels_passed, time_elapsed, parent=None):
        super().__init__(parent)
        self.levels_passed = levels_passed
        self.time_elapsed = time_elapsed
        self.initUI()

    def initUI(self): # построение интерфейса
        layout = QVBoxLayout()

        levels_label = QLabel(f"Уровней пройдено: {self.levels_passed}")
        time_label = QLabel(f"Затраченное время: {self.format_time(self.time_elapsed)}")

        layout.addWidget(levels_label)
        layout.addWidget(time_label)

        exit_button = QPushButton("Вернуться в главное меню")
        exit_button.clicked.connect(self.return_to_main_menu)

        layout.addWidget(exit_button)

        self.setLayout(layout)
        self.setWindowTitle("Результаты игры")

    def format_time(self, seconds): # форматирование времени в секундах в минуты и секунды
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes} мин. {seconds} сек."

    def return_to_main_menu(self): # возврат в меню
        self.parent().parent().stacked_widget.setCurrentIndex(0)


class PlayMode(QWidget):
    def __init__(self):
        super().__init__()
        self.end_time = None
        self.matrix = []
        self.selected_car = []
        self.buttons = []
        self.level = 1
        self.start_time = time.time()
        self.get_matrix(f'levels\{self.level}.txt')
        self.initUI()
        self.is_selected = False
        self.time_passed = 0
        self.timer = QTimer()

        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        top_panel = QWidget()
        top_layout = QHBoxLayout()
        top_panel.setLayout(top_layout)

        self.level_label = QLabel("Уровень 1")
        self.level_label.setMinimumWidth(50)  # Устанавливаем минимальную ширину для надписи с уровнем
        exit_button = QPushButton("Выход")
        exit_button.clicked.connect(self.end_game)
        self.timer_label = QLabel('Прошло: 0:0')

        top_layout.addWidget(self.level_label)
        top_layout.addWidget(self.timer_label)
        top_layout.addWidget(exit_button)

        layout.addWidget(top_panel)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)
        layout.addLayout(grid_layout)

        rows = len(self.matrix)
        cols = len(self.matrix[0])

        # Создаем кнопки для каждой ячейки матрицы и добавляем их в сетку
        for i in range(rows):
            row_buttons = []
            for j in range(cols):
                button = QPushButton()
                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                button.clicked.connect(lambda _, r=i, c=j: self.select_car(r, c))
                grid_layout.addWidget(button, i, j)
                row_buttons.append(button)

            self.buttons.append(row_buttons)

        self.update_grid()

    def update_timer(self): #обновление таймера на поле
        self.time_passed += 1
        secs = self.time_passed % 60
        mins = self.time_passed // 60
        self.timer_label.setText(f'Прошло: {mins}:{secs}')

    def keyPressEvent(self, event): #обработчик нажатий клавиш
        if self.is_selected:
            if event.key() == Qt.Key_W or event.text() == 'ц':
                self.move_car("Up")
            if event.key() == Qt.Key_S or event.text() == 'ы':
                self.move_car("Down")
            if event.key() == Qt.Key_D or event.text() == 'в':
                self.move_car("Right")
            if event.key() == Qt.Key_A or event.text() == 'ф':
                self.move_car("Left")

    def select_car(self, row, column): # функция выбора машины
        self.is_selected = True
        self.selected_car = [[row, column]]
        value = self.matrix[row][column]  # Значение текущей ячейки
        if value == 1:  # Проверяем смежные ячейки по вертикали
            for i in range(row - 1, -1, -1):
                if self.matrix[i][column] == value:
                    self.selected_car.append([i, column])
                else:
                    break
            for i in range(row + 1, len(self.matrix)):
                if self.matrix[i][column] == value:
                    self.selected_car.append([i, column])
                else:
                    break

        elif value == 2 or value == 3:  # Проверяем соседние ячейки по горизонтали
            for j in range(column - 1, -1, -1):
                if self.matrix[row][j] == value:
                    self.selected_car.append([row, j])
                else:
                    break
            for j in range(column + 1, len(self.matrix[0])):
                if self.matrix[row][j] == value:
                    self.selected_car.append([row, j])
                else:
                    break

        self.selected_car.sort()

    def move_car(self, direction): # функция пермещения машин
        car_type = self.matrix[self.selected_car[0][0]][self.selected_car[0][1]]

        if car_type == 1: # если машина вертикальная
            if direction == "Up" and self.selected_car[0][0] != 0 and 0 == \
                    self.matrix[self.selected_car[0][0] - 1][self.selected_car[0][1]]:
                for i in range(len(self.selected_car)):
                    self.matrix[self.selected_car[i][0] - 1][self.selected_car[i][1]] = car_type
                    self.matrix[self.selected_car[i][0]][self.selected_car[i][1]] = 0
                    self.selected_car[i][0] -= 1

            elif direction == "Down" and self.selected_car[-1][0] != len(self.matrix)-1 and 0 == \
                    self.matrix[self.selected_car[-1][0] + 1][self.selected_car[-1][1]]:
                for i in range(len(self.selected_car)-1, -1, -1):
                    self.matrix[self.selected_car[i][0] + 1][self.selected_car[i][1]] = car_type
                    self.matrix[self.selected_car[i][0]][self.selected_car[i][1]] = 0
                    self.selected_car[i][0] += 1

        elif car_type == 2 or car_type == 3: # если машина горизонтальная
            if direction == "Right" and self.selected_car[-1][1] != len(self.matrix[0]) - 1 and (0 == \
                    self.matrix[self.selected_car[-1][0]][self.selected_car[-1][1]+1] or 4 == \
                    self.matrix[self.selected_car[-1][0]][self.selected_car[-1][1]+1]):
                if car_type == 3 and 4 == self.matrix[self.selected_car[-1][0]][self.selected_car[-1][1]+1]:
                    self.lvl_complete()

                for i in range(len(self.selected_car)-1, -1, -1):
                    self.matrix[self.selected_car[i][0]][self.selected_car[i][1] + 1] = car_type
                    self.matrix[self.selected_car[i][0]][self.selected_car[i][1]] = 0
                    self.selected_car[i][1] += 1

            elif direction == "Left" and self.selected_car[0][1] != 0 and 0 == \
                    self.matrix[self.selected_car[0][0]][self.selected_car[0][1]-1]:
                for i in range(len(self.selected_car)):
                    self.matrix[self.selected_car[i][0]][self.selected_car[i][1] - 1] = car_type
                    self.matrix[self.selected_car[i][0]][self.selected_car[i][1]] = 0
                    self.selected_car[i][1] -= 1

        self.update_grid()

    def update_grid(self): # обновление кнопок для соответсвия изменениям
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if self.matrix[i][j] == 1:
                    self.buttons[i][j].setStyleSheet("background-color: red")
                elif self.matrix[i][j] == 2:
                    self.buttons[i][j].setStyleSheet("background-color: blue")
                elif self.matrix[i][j] == 3:
                    self.buttons[i][j].setStyleSheet("background-color: green")
                elif self.matrix[i][j] == 4:
                    self.buttons[i][j].setStyleSheet("background-color: dark-gray")
                elif self.matrix[i][j] == 5:
                    self.buttons[i][j].setStyleSheet("background-color: white")
                else:
                    self.buttons[i][j].setStyleSheet("background-color: gray")

    def lvl_complete(self): # завершение уровня
        self.level += 1
        if self.level <= 20:
            if os.path.exists(f'levels\{self.level}.txt'):
                self.get_matrix(f'levels\{self.level}.txt')
                self.selected_car = []
                self.is_selected = False
                self.update_grid()
                self.level_label.setText(f'Уровень {self.level}')
            else:
                self.end_game()
        else:
            self.end_game()

    def get_matrix(self, filename): # считывание матрицы уровня из файла
        self.matrix = []
        with open(filename, 'r') as file:
            for line in file:
                row = [int(x) for x in line.strip().split()]
                self.matrix.append(row)

    def end_game(self): # завершение игры
        elapsed_time = time.time() - self.start_time
        levels_passed = self.level - 1
        result_screen = ResultWindow(levels_passed, elapsed_time, self.parent().parent())
        self.parent().parent().stacked_widget.addWidget(result_screen)
        self.parent().parent().stacked_widget.setCurrentWidget(result_screen)


class RulesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel("Правила игры")
        label.setAlignment(Qt.AlignCenter)

        info_label = QLabel("Ваша цель вывести зеленую машину из парковки.\nЧерная клетка - это выход для машины \nЗаленая и красные машины могут двигаться "
                            "\nтолько по горизонтальной линии, cиние же машины могут \nдвигаться только по вертикальной линии.")
        info_label.setAlignment(Qt.AlignCenter)



        layout.addWidget(label)
        layout.addWidget(info_label)
        exit_button = QPushButton("Вернуться в главное меню")
        exit_button.clicked.connect(self.return_to_menu)

        layout.addWidget(exit_button)

    def return_to_menu(self):
        self.parent().parent().stacked_widget.setCurrentIndex(0)


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        label = QLabel("Парковка")
        label.setAlignment(Qt.AlignCenter)
        label.setFixedHeight(50)
        self.play_button = QPushButton("Играть")
        self.rules_button = QPushButton("Правила")
        self.exit_button = QPushButton("Выход")

        layout.addWidget(label)
        layout.addWidget(self.play_button)
        layout.addWidget(self.rules_button)
        layout.addWidget(self.exit_button)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.widget = None
        self.stacked_widget = QStackedWidget()
        self.setMinimumSize(400, 400)
        self.setWindowTitle("Парковка")

        layout = QVBoxLayout(self)
        self.setLayout(layout)
        layout.addWidget(self.stacked_widget)

        self.main_menu = MainMenu()
        self.stacked_widget.addWidget(self.main_menu)

        self.main_menu.play_button.clicked.connect(self.play) # связывание кнопки с фукнцией
        self.main_menu.rules_button.clicked.connect(self.show_rules)
        self.main_menu.exit_button.clicked.connect(lambda: QApplication.quit())

        self.show()

    def play(self): # переключение на игровое поле
        if os.path.exists(f'levels\{str(1)}.txt'): # format нужен для того, чтобы \1 не считалось спец символом
            self.widget = PlayMode()
            self.stacked_widget.addWidget(self.widget)
            self.stacked_widget.setCurrentWidget(self.widget)


    def show_rules(self): # переключение на правила
        self.widget = RulesWindow()
        self.stacked_widget.addWidget(self.widget)
        self.stacked_widget.setCurrentWidget(self.widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow() # Создание экземпляра класса игры
    sys.exit(app.exec_())
