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
        #self.labelt = QLabel("네이버 자동 로그인 후 메일함에 들어가서 스팸메일 판독 후 스팸메일을 자동 삭제해주는 기능입니다.",self)
        self.checkBox2 = QCheckBox("Mail Send", self)
        self.checkBox3 = QCheckBox("News Summarize", self)

        self.layout_1.addWidget(self.checkBox1)
        #self.layout_1.addWidget(self.labelt)
        self.layout_2.addWidget(self.checkBox2)
        self.layout_3.addWidget(self.checkBox3)

        self.frame_1.setLayout(self.layout_1)
        self.frame_2.setLayout(self.layout_2)
        self.frame_3.setLayout(self.layout_3)

        self.spliter_1 = QSplitter(Qt.Horizontal)
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
