import sys
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
import re
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QDialog
import io
from PyQt5.QtCore import *
from SubWindow import SubWindow

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Service")
        self.setupUI()

    def setupUI(self):

        self.setGeometry(800, 200, 600, 600)

        self.checkBox1 = QCheckBox("Spam Mail Delete", self)
        self.checkBox1.move(10, 20)
        self.checkBox1.resize(150, 30)
        self.checkBox1.stateChanged.connect(self.checkBoxState)

        self.checkBox2 = QCheckBox("Mail Send", self)
        self.checkBox2.move(10, 50)
        self.checkBox2.resize(150, 30)
        self.checkBox2.stateChanged.connect(self.checkBoxState)

        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

        textLabel = QLabel("제목 : ", self)
        textLabel.move(10, 300)

        self.label = QLabel("", self)
        self.label.move(70, 300)
        self.label.resize(1000, 30)

        textLabel1 = QLabel("요약 : ", self)
        textLabel1.move(10, 330)

        self.label1 = QLabel("", self)
        self.label1.move(70, 320)
        self.label1.resize(1000, 50)

        self.line = QLineEdit(self)
        self.line.move(10, 200)  # 버튼 위치
        self.line.resize(100, 30)


        self.btnRun = QPushButton("News Summarize", self)  # 버튼 텍스트
        self.btnRun.move(110, 200)  # 버튼 위치
        self.btnRun.resize(150, 30)
        self.btnRun.clicked.connect(self.btnRun_clicked)




    def checkBoxState(self):
        msg = ""
        if self.checkBox2.isChecked() == True:
            win = SubWindow()
            r = win.showModal()
        self.statusBar.showMessage(msg)

    def btnRun_clicked(self):
        newkeyword = self.line.text()
        sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

        '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        < naver 뉴스 검색시 리스트 크롤링하는 프로그램 > _select사용
        - 크롤링 해오는 것 : 링크,제목,신문사,내용요약본
        - 내용요약본  -> 정제 작업 필요
        - 리스트 -> 딕셔너리 -> df -> 엑셀로 저장
        '''''''''''''''''''''

        # 각 크롤링 결과 저장하기 위한 리스트 선언
        title_text = []
        contents_text = []
        title_list =[]
        news_list = []
        result = {}

        # 내용 정제화 함수
        def contents_cleansing(contents):
            first_cleansing_contents = re.sub('<{}><dl>.*?</a> </div> </dd> <dd>', '',
                                              str(contents)).strip()  # 앞에 필요없는 부분 제거
            second_cleansing_contents = re.sub('<ul class="relation_lst">.*?</dd>', '',
                                               first_cleansing_contents).strip()  # 뒤에 필요없는 부분 제거 (새끼 기사)
            third_cleansing_contents = re.sub('<.+?>', '', second_cleansing_contents).strip()
            contents_text.append(third_cleansing_contents)

        def crawler(newkeyword):
            url = "https://search.naver.com/search.naver?where=news&query=" + newkeyword + "&sort=1"
            response = requests.get(url)
            html = response.text

            # 뷰티풀소프의 인자값 지정
            soup = BeautifulSoup(html, 'html.parser')

            # <a>태그에서 제목과 링크주소 (a 태그 중 class 명이 news_tit인 것)
            atags = soup.find_all('a', 'news_tit')
            for atag in atags:
                title = atag.get('title')
                title_text.append(title)  # 제목


            # 본문요약본 (a 태그 중 class 명이 api_txt_lines dsc_txt_wrap인 것)
            from gensim.summarization.summarizer import summarize

            contents_lists = soup.find_all('a', 'api_txt_lines dsc_txt_wrap')
            for contents_list in contents_lists:
                contents_cleansing(contents_list)  # 본문요약 정제화



            title_list= title_text


            self.label.setText(str(title_list[0]))
            self.label1.setText(str(contents_list))



        def main():
            # query = input("검색어 입력: ")  # 네이버, 부동산...
            # info_main = input("=" * 50  + "\n" + " 뉴스요약 성공 Enter를 눌러주세요." + "\n" + "=" * 50)
            crawler(newkeyword)
        main()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()