import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType('question.ui')[0]

class AuthDialog(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initSetting()

    def initSetting(self):
        self.setWindowTitle('도움말')
        self.pushButton.clicked.connect(self.close)



if __name__ == "__main__" :

    app = QApplication(sys.argv)
    question = AuthDialog()
    question.show()
    app.exec_()