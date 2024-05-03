import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton
from PyQt5.QtCore import Qt


class MatrixGrid(QWidget):
    def __init__(self, matrix):
        super().__init__()
        self.matrix = matrix
        self.selected_car = []
        self.buttons = []
        self.initUI()
        self.is_selected = False

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        # Устанавливаем количество строк и столбцов сетки
        rows = len(self.matrix)
        cols = len(self.matrix[0])

        # Создаем кнопки для каждой ячейки матрицы и добавляем их в сетку
        for i in range(rows):
            row_buttons = []
            for j in range(cols):
                button = QPushButton()
                button.clicked.connect(lambda _, r=i, c=j: self.select_car(r, c))
                grid.addWidget(button, i, j)
                row_buttons.append(button)

            self.buttons.append(row_buttons)

        self.update_grid()

        # Устанавливаем размер окна
        self.resize(800, 600)
        # Размещаем сетку по центру
        self.setWindowTitle('Matrix Grid')
        self.show()

    def keyPressEvent(self, event):
        if self.is_selected:
            if event.key() == Qt.Key_W or event.text() == 'ц':
                self.move_car("Up")
            if event.key() == Qt.Key_S or event.text() == 'ы':
                self.move_car("Down")
            if event.key() == Qt.Key_D or event.text() == 'в':
                self.move_car("Right")
            if event.key() == Qt.Key_A or event.text() == 'ф':
                self.move_car("Left")

    def select_car(self, row, column):
        self.is_selected = True
        self.selected_car = [[row, column]]
        value = self.matrix[row][column]  # Значение текущей ячейки
        if value == 1:  # Проверяем соседние ячейки по вертикали
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

    def move_car(self, direction):
        car_type = self.matrix[self.selected_car[0][0]][self.selected_car[0][1]]

        if car_type == 1:
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

        elif car_type == 2 or car_type == 3:
            if direction == "Right" and self.selected_car[-1][1] != len(self.matrix[0]) - 1 and (0 == \
                    self.matrix[self.selected_car[-1][0]][self.selected_car[-1][1]+1] or 4 == \
                    self.matrix[self.selected_car[-1][0]][self.selected_car[-1][1]+1]):
                if car_type == 3 and 4 == self.matrix[self.selected_car[-1][0]][self.selected_car[-1][1]+1]:
                    print('lk;lkal;sk')
                    for i in range(5):
                        print(self.matrix[i])
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

    def update_grid(self):
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
                else:
                    self.buttons[i][j].setStyleSheet("background-color: gray")


def main():
    matrix = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [3, 3, 0, 1, 4, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 2, 2, 2, 0, 0],
        [0, 2, 2, 2, 0, 0]
    ]

    app = QApplication(sys.argv)
    ex = MatrixGrid(matrix)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
