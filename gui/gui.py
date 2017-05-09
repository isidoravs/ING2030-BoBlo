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
        self.connect(self.boblo, SIGNAL("invalid"), self.invalid)
        self.boblo.to_step3.clicked.connect(self.step3)
        self.boblo.to_step4.clicked.connect(self.step4)
        self.boblo.to_step5.clicked.connect(self.step5)
        self.boblo.back_to_step2.clicked.connect(self.step2)
        self.boblo.restart.clicked.connect(self.step0)
        self.boblo.options.cellClicked.connect(self.item_click)

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
        blocks = plastic_to_blocks(self.boblo.plastic)
        self.boblo.label_blocks.setText(str(blocks))
        self.boblo.label_grs2.show()
        self.boblo.label_blocks.show()

        # combinations
        self.boblo.set_combinations(blocks)

    def invalid(self):
        self.boblo.to_step4.hide()
        print("INVALID")

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

        # # images test
        # self.boblo.options.add_option(get_absolute_path("./images/sim1.png"))
        # self.boblo.options.add_option(get_absolute_path("./images/sim2.png"))
        # self.boblo.options.add_option(get_absolute_path("./images/sim3.png"))

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
        self.boblo.options.cellClicked.connect(self.item_click)
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
        self.combinations = list()

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

        # self.options = OptionsList(self)
        self.options = OptionsTable(self)
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
        self.combinations = list()
        self.label_grs1.setText(str(self.plastic))
        self.label_grs2.setText(str(self.plastic))
        self.options = OptionsTable(self)
        self.options.setGeometry(100, 170, 824, 430)
        self.options.hide()

    def set_combinations(self, blocks):
        self.all_combinations(blocks)
        if len(self.combinations) != 0:
            if len(self.combinations) == 1 and sum(self.combinations[0].values()) == 0:
                self.emit(SIGNAL("invalid"))

        else:
            self.combinations.append({8: 5, 4: 5, 2: 5, 1: 5})

        print(self.combinations)
        self.options.set_data(self.combinations)
        return

    def all_combinations(self, blocks, step=8, comb={8: 0, 4: 0, 2: 0, 1: 0}):
        '''
            Options: 4x2 (8), 2x2 (4), 2x1 (2), 1x1 (1)
            Restricciones:
            - Max. 1 de 1x1 (impar)
            - Max 5 de un tipo
            - Max 8 piezas en total
            - Max 5 entre 1x1 y 2x1
        '''
        actual_sum = sum([x[0] * x[1] for x in comb.items()])
        if step == 0:
            # restricciones

            if actual_sum == blocks:
                if comb[1] <= 1 and (comb[1] + comb[2]) <= 5 and sum(
                        comb.values()) <= 8:
                    if len([v for v in comb.values() if v > 5]) == 0:
                        self.combinations.append(comb)
            return

        else:
            max_cant = (blocks - actual_sum) // step

            if step == 8:
                next_step = 4
            elif step == 4:
                next_step = 2
            elif step == 2:
                next_step = 1
            else:
                next_step = 0

            for i in range(0, max_cant + 1):
                aux = dict(comb)
                aux[step] = i
                self.all_combinations(blocks, next_step, aux)

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


class OptionsTable(QTableWidget):
    def __init__(self, *args):
        QTableWidget.__init__(self, *args)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.horizontalHeader().hide()
        self.setIconSize(QSize(80, 80))
        self.setShowGrid(False)

    def set_data(self, data):
        self.setColumnCount(8)
        self.setRowCount(len(data))

        for r, comb in enumerate(data):
            m = 0  # 0 <= m < 8

            for n in [8, 4, 2, 1]:
                if comb[n] != 0:
                    qty = QTableWidgetItem()
                    qty.setSizeHint(QSize(100, 100))
                    icon = QIcon(
                        get_absolute_path("./images/{}x.png".format(comb[n])))
                    qty.setIcon(icon)
                    self.setItem(r, m, qty)

                    block = QTableWidgetItem()
                    block.setSizeHint(QSize(100, 100))
                    icon = QIcon(get_absolute_path("./images/boblo{}.png".format(n)))
                    block.setIcon(icon)
                    self.setItem(r, m + 1, block)

                    m += 2

        self.resizeColumnsToContents()
        self.resizeRowsToContents()


if __name__ == "__main__":
    app = QApplication([])
    gui = GUI()
    app.exec_()