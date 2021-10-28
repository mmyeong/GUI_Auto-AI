import sys
from SubWindow import SubWindow
from ThrWindow import ThrWindow
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MyWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.showMaximized()

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.setWindowTitle("AI Service")
        self.frame_1 = QFrame()
        self.frame_1.setFrameShape(QFrame.Panel | QFrame.Sunken)
        self.frame_2 = QFrame()
        self.frame_2.setFrameShape(QFrame.Panel | QFrame.Sunken)
        self.frame_3 = QFrame()
        self.frame_3.setFrameShape(QFrame.Panel | QFrame.Sunken)


        self.layout_1 = QVBoxLayout()
        self.layout_2 = QVBoxLayout()
        self.layout_3 = QVBoxLayout()

        self.checkBox1 = QCheckBox("Spam Mail Delete", self)
        self.labelt1 = QLabel("It automatically deletes spam emails after automatic login to Naver and reading the mailbox spam emails.",self)
        self.checkBox2 = QCheckBox("Mail Send", self)
        self.labelt2 = QLabel("It is a function that allows you to send mail.")
        self.checkBox3 = QCheckBox("News Summarize", self)
        self.labelt3 = QLabel("It is a function that summarizes Naver news..")

        self.checkBox1.setFont(QFont("궁서",15))
        self.checkBox2.setFont(QFont("궁서", 15))
        self.checkBox3.setFont(QFont("궁서", 15))
        self.checkBox1.setStyleSheet("Color : green")
        self.checkBox2.setStyleSheet("Color : green")
        self.checkBox3.setStyleSheet("Color : green")

        self.layout_1.addWidget(self.checkBox1)
        self.layout_1.addWidget(self.labelt1)
        self.layout_2.addWidget(self.checkBox2)
        self.layout_2.addWidget(self.labelt2)
        self.layout_3.addWidget(self.checkBox3)
        self.layout_3.addWidget(self.labelt3)

        self.frame_1.setLayout(self.layout_1)
        self.frame_2.setLayout(self.layout_2)
        self.frame_3.setLayout(self.layout_3)

        self.spliter_1 = QSplitter(Qt.Vertical)
        self.spliter_1.addWidget(self.frame_1)
        self.spliter_1.addWidget(self.frame_2)
        self.spliter_1.addWidget(self.frame_3)

        self.main_layout.addWidget(self.spliter_1)

        self.checkBox1.stateChanged.connect(self.checkBoxState)
        self.checkBox2.stateChanged.connect(self.checkBoxState)
        self.checkBox3.stateChanged.connect(self.checkBoxState)
        self.setLayout(self.main_layout)
        self.resize(500, 500)

    def checkBoxState(self):
        msg = ""
        if self.checkBox2.isChecked() == True:
            win = SubWindow()
            r = win.showModal()
        if self.checkBox3.isChecked() == True:
            win = ThrWindow()
            r = win.showModal()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()
