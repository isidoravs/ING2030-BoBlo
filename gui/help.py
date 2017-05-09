from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

data = {'col1': ['1', '2', '3'], 'col2': ['4', '5', '6'],
        'col3': ['7', '8', '9']}


class MyTable(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.setmydata()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.horizontalHeader().hide()

    def setmydata(self):

        horHeaders = []
        for n, key in enumerate(sorted(self.data.keys())):
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)


def main(args):
    app = QApplication(args)
    table = MyTable(data, 5, 3)
    table.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main(sys.argv)