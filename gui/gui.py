from PyQt4.QtGui import QWidget, QLabel, QPixmap, QMainWindow, QApplication
from PyQt4.QtGui import QRadioButton, QLineEdit, QPushButton, QDesktopWidget
from PyQt4.QtGui import QListWidget, QListWidgetItem, QIcon, QFont
from PyQt4.QtGui import QTableWidget, QTableWidgetItem, QAbstractItemView
from PyQt4.QtCore import Qt, SIGNAL, QSize
from .utils import plastic_to_blocks
import os
# from .file import Class


def get_absolute_path(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.boblo = BoBlo()
        self.connections()
        self.boblo.show()
        self.boblo.raise_()

    def connections(self):
        self.connect(self.boblo, SIGNAL("sim"), self.step2)
        self.boblo.to_step3.clicked.connect(self.step3)
        self.boblo.to_step4.clicked.connect(self.step4)
        self.boblo.to_step5.clicked.connect(self.step5)
        self.boblo.back_to_step2.clicked.connect(self.step2)
        self.boblo.restart.clicked.connect(self.step0)
        self.boblo.options.itemClicked.connect(self.item_click)

    def step2(self):
        '''
            Has reciclado:
        '''
        # from step 1
        self.boblo.pic1.hide()
        self.boblo.text1.hide()

        # from step 4
        self.boblo.text4.hide()
        self.boblo.to_step4.hide()
        self.boblo.back_to_step2.hide()
        self.boblo.pic2.hide()
        self.boblo.label_grs2.hide()
        self.boblo.label_blocks.hide()

        self.boblo.label_grs1.show()
        self.boblo.text2.show()
        self.boblo.text3.show()
        self.boblo.to_step3.show()

    def step3(self):
        '''
            Con tus X gramos de plastico...
        '''
        self.boblo.simulation = False

        self.boblo.to_step3.hide()
        self.boblo.text2.hide()
        self.boblo.text3.hide()
        self.boblo.label_grs1.hide()

        self.boblo.text4.show()
        self.boblo.to_step4.show()
        self.boblo.back_to_step2.show()
        self.boblo.pic2.show()

        self.boblo.label_grs2.setText(str(self.boblo.plastic))
        self.boblo.label_blocks.setText(str(plastic_to_blocks(self.boblo.plastic)))
        self.boblo.label_grs2.show()
        self.boblo.label_blocks.show()

    def step4(self):
        '''
            Elige tu combinación
        '''
        self.boblo.text4.hide()
        self.boblo.to_step4.hide()
        self.boblo.back_to_step2.hide()
        self.boblo.pic2.hide()

        self.boblo.label_grs2.hide()
        self.boblo.label_blocks.hide()

        self.boblo.text5.show()

        # combinaciones
        self.boblo.options.show()

        # images test
        self.boblo.options.add_option(get_absolute_path("./images/sim1.png"))
        self.boblo.options.add_option(get_absolute_path("./images/sim2.png"))
        self.boblo.options.add_option(get_absolute_path("./images/sim3.png"))

    def step5(self):
        self.boblo.text5.hide()
        self.boblo.to_step5.hide()
        self.boblo.options.hide()

        self.boblo.text6.show()
        self.boblo.text7.show()
        self.boblo.restart.show()

    def step0(self):
        # clean screen
        self.boblo.text6.hide()
        self.boblo.text7.hide()
        self.boblo.restart.hide()

        # restart variables
        self.boblo.restart_values()
        self.boblo.text1.show()
        self.boblo.pic1.show()

    def item_click(self, item):
        self.boblo.to_step5.show()


class BoBlo(QWidget):
    '''
        Revisar layouts para proporciones
    '''
    def __init__(self):
        super().__init__()
        self.setFixedSize(1024, 768)
        self.setWindowTitle('BoBlo - Bottle Blocks')
        self.setWindowIcon(QIcon(get_absolute_path('images/icon2.png')))
        self.screenShape = QDesktopWidget().screenGeometry()
        self.bg_width = 1024
        self.bg_height = 768
        # self.resize(self.screenShape.width(), self.screenShape.height())

        self.simulation = False

        self.plastic = 0.0

        self.button_stylesheet = "QPushButton {background-color: #8FCBF4;" \
                                 "border-style: outset;" \
                                 "border-width: 2px;" \
                                 "border-radius: 10px;" \
                                 "border-color: #C6E2FF;" \
                                 "font: bold 15pt \"Comic Sans MS\";" \
                                 "min-width: 10em;" \
                                 "padding: 6px;}" \
                                 "QPushButton:pressed {background-color: #4F94CD}"

        self.background = QLabel(self)
        self.background.setGeometry(0, 0, self.bg_width, self.bg_height)
        self.background.setPixmap(QPixmap(get_absolute_path(
            "./images/background.jpg")).scaled(self.bg_width, self.bg_height))

        self.label_grs1 = QLabel(str(self.plastic), self)
        self.label_grs1.setFont(QFont("Comic Sans MS", 40, QFont.Bold))
        self.label_grs1.setGeometry(120, 270, 310, 120)
        self.label_grs1.setAlignment(Qt.AlignRight)
        self.label_grs1.hide()

        self.label_grs2 = QLabel(str(self.plastic), self)
        self.label_grs2.setFont(QFont("Comic Sans MS", 40, QFont.Bold))
        self.label_grs2.setGeometry(300, 58, 310, 120)
        self.label_grs2.setAlignment(Qt.AlignCenter)
        self.label_grs2.hide()

        self.label_blocks = QLabel(str(plastic_to_blocks(self.plastic)), self)
        self.label_blocks.setFont(QFont("Comic Sans MS", 50, QFont.Bold))
        self.label_blocks.setGeometry(180, 330, 310, 150)
        self.label_blocks.setAlignment(Qt.AlignRight)
        self.label_blocks.hide()

        self.text1 = QLabel(self)
        self.text1.move(50, 100)
        self.text1.setPixmap(QPixmap(get_absolute_path("./images/text1.png")))

        self.pic1 = QLabel(self)
        self.pic1.move(550, 450)
        self.pic1.setPixmap(QPixmap(get_absolute_path("./images/image_step1.png")))

        self.text2 = QLabel(self)
        self.text2.move(50, 50)
        self.text2.setPixmap(QPixmap(get_absolute_path("./images/text2.png")))
        self.text2.hide()

        self.text3 = QLabel(self)
        self.text3.move(410, 260)
        self.text3.setPixmap(QPixmap(get_absolute_path("./images/text3.png")))
        self.text3.hide()

        self.text4 = QLabel(self)
        self.text4.move(50, 50)
        self.text4.setPixmap(QPixmap(get_absolute_path("./images/text4.png")))
        self.text4.hide()

        self.pic2 = QLabel(self)
        self.pic2.move(550, 350)
        self.pic2.setPixmap(
            QPixmap(get_absolute_path("./images/boblo1.png")))
        self.pic2.hide()

        self.text5 = QLabel(self)
        self.text5.move(50, 50)
        self.text5.setPixmap(QPixmap(get_absolute_path("./images/text5.png")))
        self.text5.hide()

        self.to_step3 = QPushButton("&Quiero mis piezas", self)
        self.to_step3.setGeometry(600, 570, 300, 90)
        self.to_step3.setStyleSheet(self.button_stylesheet)
        self.to_step3.hide()

        self.icon_arrow = QIcon(get_absolute_path("./images/arrow.png"))
        self.to_step4 = QPushButton("", self)
        self.to_step4.setIcon(self.icon_arrow)
        self.to_step4.setIconSize(QSize(250, 60))
        self.to_step4.setGeometry(600, 570, 300, 90)
        self.to_step4.setStyleSheet(self.button_stylesheet)
        self.to_step4.hide()

        self.icon_arrowi = QIcon(get_absolute_path("./images/arrowi.png"))
        self.back_to_step2 = QPushButton("", self)
        self.back_to_step2.setIcon(self.icon_arrowi)
        self.back_to_step2.setIconSize(QSize(250, 60))
        self.back_to_step2.setGeometry(124, 570, 300, 90)
        self.back_to_step2.setStyleSheet(self.button_stylesheet)
        self.back_to_step2.hide()

        self.to_step5 = QPushButton("", self)
        self.to_step5.setIcon(self.icon_arrow)
        self.to_step5.setIconSize(QSize(250, 60))
        self.to_step5.setGeometry(620, 610, 300, 90)
        self.to_step5.setStyleSheet(self.button_stylesheet)
        self.to_step5.hide()

        self.options = OptionsList(self)
        self.options.setGeometry(100, 170, 824, 430)
        self.options.hide()

        self.text6 = QLabel(self)
        self.text6.move(50, 100)
        self.text6.setPixmap(QPixmap(get_absolute_path("./images/text6.png")))
        self.text6.hide()

        self.text7 = QLabel(self)
        self.text7.move(60, 480)
        self.text7.setPixmap(QPixmap(get_absolute_path("./images/text7.png")))
        self.text7.hide()

        self.restart = QPushButton("&OK", self)
        self.restart.setGeometry(600, 570, 300, 90)
        self.restart.setStyleSheet(self.button_stylesheet)
        self.restart.hide()

    def restart_values(self):
        self.plastic = 0.0
        self.label_grs1.setText(str(self.plastic))
        self.label_grs2.setText(str(self.plastic))

    def keyPressEvent(self, QKeyEvent):

        if QKeyEvent.text() == "s":
            if self.simulation:
                # solo dos botellas aprox. 500 ml
                if self.plastic == 0:
                    self.plastic += 30.5
                else:
                    self.plastic += 26.3

                self.label_grs1.setText(str(self.plastic))
                self.label_grs2.setText(str(self.plastic))

            else:
                self.simulation = True
                self.emit(SIGNAL("sim"))


class OptionsList(QListWidget):

    def __init__(self, parent):
        QListWidget.__init__(self, parent)
        self.setIconSize(QSize(800, 80))

    def add_option(self, path):
        try:
            with open(path, "r"):
                pass
        except FileNotFoundError as err:
            print(err)
            return

        item = QListWidgetItem()
        item.setSizeHint(QSize(800, 100))
        icon = QIcon(path)
        item.setIcon(icon)
        self.addItem(item)


# class OptionsTable(QTableWidget):
#     def __init__(self, data, *args):
#         QTableWidget.__init__(self, *args)
#         self.data = data
#         self.setmydata()
#         self.resizeColumnsToContents()
#         self.resizeRowsToContents()
#         self.setSelectionBehavior(QAbstractItemView.SelectRows)
#
#     def setmydata(self):
#
#         horHeaders = []
#         for n, key in enumerate(sorted(self.data.keys())):
#             horHeaders.append(key)
#             for m, item in enumerate(self.data[key]):
#                 newitem = QTableWidgetItem(item)
#                 self.setItem(m, n, newitem)
#         self.setHorizontalHeaderLabels(horHeaders)


if __name__ == "__main__":
    app = QApplication([])
    gui = GUI()
    app.exec_()