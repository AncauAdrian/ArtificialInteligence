from UI import UI
from PyQt5 import QtWidgets
import sys

def main():
    app = QtWidgets.QApplication([])
    application = UI()
    application.show()
    sys.exit(app.exec())

main()

