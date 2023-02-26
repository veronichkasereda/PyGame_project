import sys
import shutil

from PyQt5.QtWidgets import QApplication, QMainWindow
from game_run_widget import Ui_Dialog
from pygame_code import *


class QWidget(QMainWindow, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Загружаем дизайн
        self.comboBox.addItems(['Выберите уровень', '1 уровень', '2 уровень', '3 уровень', '4 уровень', '5 уровень'])
        self.pushButton.clicked.connect(self.game_on)
        self.comboBox.currentTextChanged.connect(self.run)
        self.close()

    def run(self, file_name):
        try:
            #копирования карты нужного уровня в файл для загрузки уровня в игру
            shutil.copyfile(f'levels/{file_name}', 'data/Карта')

        except Exception as ex:
            print(ex)
    #вызов игрового цикла основного файла при нажатии кнопки
    def game_on(self):
        main()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QWidget()
    ex.show()
    sys.exit(app.exec_())
