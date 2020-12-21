import os
import sys
import random
from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt
import numpy as np
from sklearn.cluster import KMeans
from PyQt5 import uic
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, \
    QLabel, QVBoxLayout, QFileDialog


def img_to_palette(image, n):
    img = Image.open(image)
    # считывание картинки как вектора в массив
    vec = np.array(img)
    vec = vec.reshape(-1, 3)
    # нахождение n доминантных цветов изображения
    model = KMeans(n_clusters=n).fit(vec)
    colors = model.cluster_centers_
    im = Image.new('RGBA', (100 * len(colors), 100))
    draw = ImageDraw.Draw(im)
    for coord, color in enumerate(colors):
        # компиляция цветов в палитру
        color = tuple([int(x) for x in color])
        draw.rectangle([(100 * coord, 0), (100 * (coord + 1),
                                           100 * (coord + 1))], tuple(color))
    return im


class Practice(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('testing.ui', self)
        oImage = QImage("фон_тест.jpg")
        sImage = oImage.scaled(QSize(1050, 600))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)
        self.dct = {'00.jpg': '3', '01.jpg': '6', '02.jpg': '6', '03.jpg': '3',
                    '04.jpg': '4', '05.jpg': '5', '06.jpg': '4', '07.jpg': '4',
                    '08.jpg': '6', '09.jpg': '5', '10.jpg': '6', '11.jpg': '4',
                    '12.jpg': '3', '13.jpg': '3', '14.jpg': '4', '15.jpg': '6',
                    '16.jpg': '2', '17.jpg': '3', '18.jpg': '5', '19.jpg': '4',
                    '20.jpg': '4', '21.jpg': '6', '22.jpg': '6', '23.jpg': '6',
                    '24.jpg': '2', '25.jpg': '5', '26.jpg': '6', '27.jpg': '4',
                    '28.jpg': '2', '29.jpg': '2', '30.jpg': '2', '31.jpg': '5',
                    '32.jpg': '4', '33.jpg': '1', '34.jpg': '4', '35.jpg': '2',
                    '36.jpg': '4', '37.jpg': '4', '38.jpg': '4', '39.jpg': '2',
                    '40.jpg': '4', '41.jpg': '5', '42.jpg': '4', '43.jpg': '3',
                    '44.jpg': '3', '45.jpg': '3', '46.jpg': '3', '47.jpg': '1',
                    '48.jpg': '3', '49.jpg': '6', '50.jpg': '5', '51.jpg': '3',
                    '52.jpg': '2', '53.jpg': '3', '54.jpg': '3', '55.jpg': '5',
                    '56.jpg': '3', '57.jpg': '2', '58.jpg': '4', '59.jpg': '6',
                    '60.jpg': '4', '61.jpg': '4', '62.jpg': '2', '63.jpg': '2',
                    '64.jpg': '4', '65.jpg': '2', '66.jpg': '2', '67.jpg': '2',
                    '68.jpg': '2', '69.jpg': '5', '70.jpg': '4', '71.jpg': '2',
                    '72.jpg': '5', '73.jpg': '2', '74.jpg': '2', '75.jpg': '2',
                    '76.jpg': '5', '77.jpg': '6', '78.jpg': '5', '79.jpg': '5',
                    '80.jpg': '4', '81.jpg': '4', '82.jpg': '6', '83.jpg': '4',
                    '84.jpg': '6', '85.jpg': '6', '86.jpg': '4', '87.jpg': '4',
                    '88.jpg': '4', '89.jpg': '1', '90.jpg': '1', '91.jpg': '2',
                    '92.jpg': '3', '93.jpg': '5'}
        self.initUI()

    def initUI(self):
        self.setFixedSize(1050, 600)
        self.btn.clicked.connect(self.check_answer)
        self.exit.clicked.connect(self.out)
        self.counter = 0
        self.lst = []
        self.generate()

    def generate(self):
        self.flag = True
        while self.flag:
            # вбор случайного изображения из словаря и проверка на повторение
            self.pic = random.choice(list(self.dct.keys()))
            if self.pic not in self.lst:
                self.flag = False
        self.filename = os.path.join('pictures', self.pic)
        self.pixmap = QPixmap(self.filename)
        self.piclbl.setPixmap(self.pixmap.scaled(
            601, 411, Qt.KeepAspectRatio, Qt.FastTransformation))
        self.lst.append(self.pic)

    def out(self):
        self.w = Window()
        self.close()
        self.w.show()

    def check_answer(self):
        if len(self.lst) == len(self.dct.keys()):
            self.piclbl.setPixmap(QPixmap(os.path.join('pictures', 'end.jpg')))
        elif str(self.answer.toPlainText()).lower() == self.dct[self.pic]:
            self.wrong.setText('')
            self.counter += 1
            self.count.setText(str(self.counter))
            self.answer.setText('')
            self.generate()
        else:
            self.wrong.setText('Неверно!')


class Palette_generator(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('palette_generator.ui', self)
        oImage = QImage("фон.jpg")
        sImage = oImage.scaled(QSize(1050, 600))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)
        self.initUI()

    def initUI(self):
        self.setFixedSize(1050, 600)
        self.fname = None
        self.image = None
        self.n = 3
        self.horizontalSlider.valueChanged.connect(self.num)
        self.exitButton.clicked.connect(self.exit)
        self.selectButton.clicked.connect(self.pick)
        self.loadButton.clicked.connect(self.show_palette)
        self.saveButton.clicked.connect(self.save_palette)

    def pick(self):
        self.fname = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Картинка JPG(*.jpg);;Все файлы(*)')
        self.pixmap = QPixmap(self.fname[0])
        self.imagelbl.setPixmap(self.pixmap.scaled(
            593, 353, Qt.KeepAspectRatio, Qt.FastTransformation))

    def show_palette(self):
        if self.fname is not None:
            self.image = img_to_palette(self.fname[0], self.n)
            self.qim = ImageQt(self.image)
            self.pix = QPixmap.fromImage(self.qim)
            self.palettelbl.setPixmap(self.pix.scaled(
                662, 51, Qt.KeepAspectRatio, Qt.FastTransformation))

    def save_palette(self):
        if self.image is not None:
            self.sve = QFileDialog.getSaveFileName(
                self, 'Сохранить картинку', 'palette',
                'Картинка png(*.png);;Все файлы(*)')
            if self.sve[0] != '':
                self.image.save(self.sve[0], 'png')

    def num(self, n):
        # замена текста в label в зависимости от положения ползунка
        self.numbers.setText(str(n))
        self.n = n

    def exit(self):
        self.w = Window()
        self.hide()
        self.w.show()


class Dict(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('short.ui', self)
        oImage = QImage("краткая памятка.jpg")
        sImage = oImage.scaled(QSize(1050, 600))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)
        self.initUI()

    def initUI(self):
        self.backButton.clicked.connect(self.back)
        # установка гиперссылок
        self.label.setText('<a style="color: rgb(163, 231, 226);"'
                           ' href="https://colorschemedesigner.com/csd-3.5/"> '
                           'колесо для подбора палитр '
                           ' палитр')
        self.label.setOpenExternalLinks(True)
        self.label_2.setText('<a style="color: rgb(163, 231, 226);" '
                             'href='
                             '"https://color.adobe.com/ru/create/color-wheel">'
                             ' ещё одно колесо для подбора')
        self.label_2.setOpenExternalLinks(True)
        self.label_3.setText('<a style="color: rgb(163, 231, 226);'
                             '" href="https://colorhunt.co/palettes">'
                             ' библиотека готовых палитр')
        self.label_3.setOpenExternalLinks(True)
        self.setFixedSize(1050, 600)

    def back(self):
        self.w = Window()
        self.w.show()
        self.hide()


class Theory(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('test.ui', self)
        self.img = QPixmap("theory.png")
        self.setFixedSize(1065, 600)
        # создание прокручиваемого ползунком окна
        self.label = QLabel(self)
        self.label.setPixmap(self.img)
        self.label.resize(1060, 600)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.resize(1065, 600)
        self.scrollArea.setWidget(self.label)
        self.l = QVBoxLayout(self)
        self.l.addWidget(self.scrollArea)
        if self.close():
            self.w = Window()
            self.w.show()
            self.hide()


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('startwindow.ui', self)
        oImage = QImage("фон с колесом.jpg")
        sImage = oImage.scaled(QSize(1050, 600))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)
        self.initUI()

    def initUI(self):
        self.setFixedSize(1050, 600)
        self.theoryButton.clicked.connect(self.open_all)
        self.practiceButton.clicked.connect(self.open_all)
        self.exitButton.clicked.connect(self.open_all)
        self.directoryButton.clicked.connect(self.open_all)
        self.pickButton.clicked.connect(self.open_all)

    def open_all(self):
        if self.sender() == self.theoryButton:
            self.w = Theory()
        elif self.sender() == self.practiceButton:
            self.w = Practice()
        elif self.sender() == self.exitButton:
            self.close()
        elif self.sender() == self.directoryButton:
            self.w = Dict()
        elif self.sender() == self.pickButton:
            self.w = Palette_generator()
        self.w.show()
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec())
