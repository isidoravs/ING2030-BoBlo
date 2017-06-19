from PyQt4.QtGui import QWidget, QLabel, QPixmap, QMainWindow, QApplication
from PyQt4.QtGui import QRadioButton, QLineEdit, QPushButton, QDesktopWidget
from PyQt4.QtGui import QListWidget, QListWidgetItem, QIcon, QFont, QSound
from PyQt4.QtGui import QTableWidget, QTableWidgetItem, QAbstractItemView
from PyQt4.QtCore import Qt, SIGNAL, QSize, QObject, pyqtSignal, pyqtSlot
from PyQt4.QtCore import QTimer, QThread
from .utils import plastic_to_blocks
from time import sleep
import serial
import os
# from .file import Class


def get_absolute_path(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)

        self.boblo = BoBlo()
        self.connections()

        self.new_user = False

        self.boblo.show()
        self.boblo.raise_()

    def connections(self):
        self.connect(self.boblo, SIGNAL("invalid"), self.invalid)
        self.connect(self.boblo, SIGNAL("weight"), self.check_step)
        self.boblo.to_step3.clicked.connect(self.step3)
        self.boblo.to_step4.clicked.connect(self.step4)
        self.boblo.to_step5.clicked.connect(self.step_process1)
        self.boblo.back_to_step2.clicked.connect(self.step2)
        self.boblo.restart.clicked.connect(self.step0)
        self.boblo.options.cellClicked.connect(self.item_click)

    def check_step(self):
        if not self.new_user:
            self.new_user = True
            self.step2()

    def step2(self):
        '''
            Has reciclado:
        '''
        # from step 1
        self.boblo.pic1.hide()
        self.boblo.text1.hide()
        self.boblo.text_dato.hide()

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

    def step_process1(self):
        self.boblo.text5.hide()
        self.boblo.to_step5.hide()
        self.boblo.options.hide()
        self.boblo.audio.play()

        self.boblo.text_process.show()
        self.timer.singleShot(2000, self.step_process2)

    def step_process2(self):
        self.boblo.text_process.setPixmap(
            QPixmap(get_absolute_path("./images/process2.png")))
        self.timer.singleShot(2000, self.step_process3)

    def step_process3(self):
        self.boblo.text_process.setPixmap(
            QPixmap(get_absolute_path("./images/process3.png")))
        self.timer.singleShot(2000, self.step5)

    def step5(self):
        self.boblo.text_process.hide()

        self.boblo.text6.show()
        self.boblo.text7.show()
        self.boblo.restart.show()
        self.dispenser()

    def dispenser(self):
        piezas = 2
        for i in range(piezas):
            self.boblo.weight_monitor.arduino.write(b'd')
            sleep(2)

    def step0(self):
        # clean screen
        self.boblo.text6.hide()
        self.boblo.text7.hide()
        self.boblo.restart.hide()

        # restart variables
        self.boblo.restart_values()
        self.boblo.options.cellClicked.connect(self.item_click)
        self.text_process.setPixmap(
            QPixmap(get_absolute_path("./images/process1.png")))
        self.boblo.text1.show()
        self.boblo.text_dato.show()
        self.boblo.pic1.show()
        self.new_user = False

    def item_click(self, item):
        self.boblo.to_step5.show()

    def closeEvent(self, *args, **kwargs):
        self.boblo.weight_monitor.arduino.close()


class BoBlo(QWidget):
    '''
        Revisar layouts para proporciones
    '''
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 100, 1024, 768)
        self.setWindowTitle('BoBlo - Bottle Blocks')
        self.setWindowIcon(QIcon(get_absolute_path('images/icon2.png')))
        self.screenShape = QDesktopWidget().screenGeometry()
        self.bg_width = 1280
        self.bg_height = 990
        # self.resize(self.screenShape.width(), self.screenShape.height())

        self.combinations = list()

        self.plastic = 0

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
        self.background.setGeometry(375, 0, self.bg_width, self.bg_height)
        self.background.setPixmap(QPixmap(get_absolute_path(
            "./images/background.jpg")).scaled(self.bg_width, self.bg_height))

        self.label_grs1 = QLabel(str(self.plastic), self)
        self.label_grs1.setFont(QFont("Comic Sans MS", 40, QFont.Bold))
        self.label_grs1.setGeometry(640, 270, 310, 120)
        self.label_grs1.setAlignment(Qt.AlignRight)
        self.label_grs1.hide()

        self.label_grs2 = QLabel(str(self.plastic), self)
        self.label_grs2.setFont(QFont("Comic Sans MS", 40, QFont.Bold))
        self.label_grs2.setGeometry(820, 58, 310, 120)
        self.label_grs2.setAlignment(Qt.AlignCenter)
        self.label_grs2.hide()

        self.label_blocks = QLabel(str(plastic_to_blocks(self.plastic)), self)
        self.label_blocks.setFont(QFont("Comic Sans MS", 50, QFont.Bold))
        self.label_blocks.setGeometry(700, 330, 310, 150)
        self.label_blocks.setAlignment(Qt.AlignRight)
        self.label_blocks.hide()

        self.text_dato = QLabel(self)
        self.text_dato.move(570, 550)
        self.text_dato.setPixmap(QPixmap(get_absolute_path("./images/dato1.png")))

        self.text1 = QLabel(self)
        self.text1.move(570, 100)
        self.text1.setPixmap(QPixmap(get_absolute_path("./images/text1.png")))

        self.pic1 = QLabel(self)
        self.pic1.move(1070, 400)
        self.pic1.setPixmap(QPixmap(get_absolute_path("./images/image_step1.png")))

        self.text2 = QLabel(self)
        self.text2.move(570, 50)
        self.text2.setPixmap(QPixmap(get_absolute_path("./images/text2.png")))
        self.text2.hide()

        self.text3 = QLabel(self)
        self.text3.move(930, 260)
        self.text3.setPixmap(QPixmap(get_absolute_path("./images/text3.png")))
        self.text3.hide()

        self.text4 = QLabel(self)
        self.text4.move(570, 50)
        self.text4.setPixmap(QPixmap(get_absolute_path("./images/text4.png")))
        self.text4.hide()

        self.pic2 = QLabel(self)
        self.pic2.move(1070, 350)
        self.pic2.setPixmap(
            QPixmap(get_absolute_path("./images/boblo1.png")))
        self.pic2.hide()

        self.text5 = QLabel(self)
        self.text5.move(570, 50)
        self.text5.setPixmap(QPixmap(get_absolute_path("./images/text5.png")))
        self.text5.hide()

        self.to_step3 = QPushButton("&Quiero mis piezas", self)
        self.to_step3.setGeometry(1120, 570, 300, 90)
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
        self.back_to_step2.setGeometry(644, 570, 300, 90)
        self.back_to_step2.setStyleSheet(self.button_stylesheet)
        self.back_to_step2.hide()

        self.to_step5 = QPushButton("", self)
        self.to_step5.setIcon(self.icon_arrow)
        self.to_step5.setIconSize(QSize(250, 60))
        self.to_step5.setGeometry(1140, 610, 300, 90)
        self.to_step5.setStyleSheet(self.button_stylesheet)
        self.to_step5.hide()

        # self.options = OptionsList(self)
        self.options = OptionsTable(self)
        self.options.setGeometry(620, 170, 824, 430)
        self.options.hide()

        self.text6 = QLabel(self)
        self.text6.move(570, 100)
        self.text6.setPixmap(QPixmap(get_absolute_path("./images/text6.png")))
        self.text6.hide()

        self.text7 = QLabel(self)
        self.text7.move(580, 480)
        self.text7.setPixmap(QPixmap(get_absolute_path("./images/text7.png")))
        self.text7.hide()

        self.text_process = QLabel(self)
        self.text_process.move(570, 480)
        self.text_process.setPixmap(
            QPixmap(get_absolute_path("./images/process1.png")))
        self.text_process.hide()

        self.restart = QPushButton("&OK", self)
        self.options.setGeometry(1120, 170, 824, 430)
        self.restart.setStyleSheet(self.button_stylesheet)
        self.restart.hide()

        self.audio = QSound(get_absolute_path("./audio/boblo.wav"))

        # threading
        self.start_thread()

    def restart_values(self):
        self.plastic = 0
        self.combinations = list()
        self.label_grs1.setText(str(self.plastic))
        self.label_grs2.setText(str(self.plastic))
        self.options = OptionsTable(self)
        self.options.setGeometry(620, 170, 824, 430)
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

    def start_thread(self):
        self.weight_monitor = ArduinoMonitor()
        self.t = QThread(self)
        self.weight_monitor.weight_signal.connect(self.update_weight)
        self.weight_monitor.moveToThread(self.t)
        self.t.started.connect(self.weight_monitor.check_weight)
        self.t.start()

    @pyqtSlot(str)
    def update_weight(self, grs):
        # actualizar peso en interfaz
        if grs != "Exito":
            self.plastic = int(grs)
            self.label_grs1.setText(str(self.plastic))
            self.label_grs2.setText(str(self.plastic))
            if int(grs) != 0:
                self.emit(SIGNAL("weight"))
        else:
            print(grs)


class ArduinoMonitor(QObject):
    weight_signal = pyqtSignal(str)  # args
    arduino = serial.Serial('COM4', 38400, timeout=1.0)

    @pyqtSlot()
    def check_weight(self):
        while True:
            line = self.arduino.readline()  # bytes
            weight = line.decode('utf-8').strip()
            if weight == "1" or weight == "-0":
                weight = "0"

            if weight != "":
                # print(weight, "gr.")
                self.weight_signal.emit(weight)


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