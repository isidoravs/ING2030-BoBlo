from gui import GUI, run
from PyQt4.QtCore import QObject, SIGNAL


class BoBlo(QObject):
    '''
        Clase principal
    '''
    def __init__(self):
        super().__init__()


class BoBloGui(GUI):
    def __init__(self):
        super().__init__()

if __name__ == "__main__":
    run(BoBloGui)