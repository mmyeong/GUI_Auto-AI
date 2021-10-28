import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import requests
from bs4 import BeautifulSoup
import bs4.element

class ThrWindow(QDialog):
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


        self.layout_1 = QVBoxLayout()
        self.layout_2 = QVBoxLayout()

        self.label1 = QLabel("요약본을 보고 싶은 분야의 숫자를 입력하세요.\n\n정치(0), 경제(1), 사회(2), 생활/문화(3), 세계(4)", self)
        self.label1.setFont(QFont("", 12))
        self.line1 = QLineEdit(self)
        self.btnRun = QPushButton("뉴스요약", self)  # 버튼 텍스트
        self.btnRun.clicked.connect(self.btnRun_clicked)
        self.label2 = QTextBrowser(self)
        self.label3 = QTextBrowser(self)
        self.label4 = QTextBrowser(self)

        self.layout_1.addWidget(self.label1)
        self.layout_1.addWidget(self.line1)
        self.layout_1.addWidget(self.btnRun)
        self.layout_2.addWidget(self.label2)
        self.layout_2.addWidget(self.label3)
        self.layout_2.addWidget(self.label4)

        self.frame_1.setLayout(self.layout_1)
        self.frame_2.setLayout(self.layout_2)

        self.spliter_1 = QSplitter(Qt.Vertical)
        self.spliter_1.addWidget(self.frame_1)
        self.spliter_1.addWidget(self.frame_2)

        self.main_layout.addWidget(self.spliter_1)
        self.setLayout(self.main_layout)
        self.resize(500, 500)

    def btnRun_clicked(self):
        news_list3 = []
        newsCr = self.line1.text()

        def newsSummarize(newsCr):
            try:
                tonewsCr = newsCr

                # BeautifulSoup
                def get_soup_obj(url):
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/63.0.3239.132 Safari/537.36'}
                    res = requests.get(url, headers=headers)
                    soup = BeautifulSoup(res.text, 'html.parser')

                    return soup

                # 뉴스 정보
                def get_top3_news_info(sec, sid):
                    sid = '10' + tonewsCr
                    # 속보(경제)
                    sec_url = "https://news.naver.com/main/list.nhn?mode=LSD&mid=sec" \
                              + '&sid1=' \
                              + sid

                    # 상위 뉴스 HTML 가져오기
                    soup = get_soup_obj(sec_url)

                    # 해당 분야 상위 뉴스 3개
                    news_list3 = []
                    lis3 = soup.find('ul', class_='type06_headline').find_all('li', limit=3)

                    for li in lis3:
                        # title 뉴스제목 news_url : 뉴스 URL, image_url : 이미지 URL

                        news_info = {
                            "title": li.img.attrs.get('alt') if li.img else li.a.text.replace("\n", "").replace(
                                "\t",
                                "").replace(
                                "\r", ""),
                            "date": li.find(class_="date").text,
                            "news_url": li.a.attrs.get('href'),
                            "image_url": li.img.attrs.get('src')
                        }
                        news_list3.append(news_info)


                    return news_list3

                # 뉴스 본문
                def get_news_contents(url):
                    soup = get_soup_obj(url)
                    body = soup.find('div', class_='_article_body_contents')

                    news_contents = ''
                    for content in body:
                        if type(content) is bs4.element.NavigableString and len(content) > 50:
                            # content.strip() : whitepace 제거
                            # 뉴스 요약을 위하여 '.' 마침표 뒤에 한칸을 띄워 문장을 구분하도록 함
                            news_contents += content.strip() + ' '

                    return news_contents

                def get_naver_news_top3():
                    # 뉴스 결과 담기
                    news_dic = dict()

                    # sections = '경제'
                    sections = ['Eco']
                    sections_ids = ['101']

                    for sec, sid in zip(sections, sections_ids):
                        news_info = get_top3_news_info(sec, sid)

                        for news in news_info:
                            # 뉴스 본문
                            news_url = news['news_url']
                            news_contents = get_news_contents(news_url)

                            # 뉴스 정보 저장
                            news['news_contents'] = news_contents

                        news_dic[sec] = news_info

                    return news_dic

                # 호출 상위 3개 뉴스 크롤링
                news_dic = get_naver_news_top3()
                # 뉴스 요약
                from gensim.summarization.summarizer import summarize

                # section 지정
                my_section = 'Eco'
                news_list3 = news_dic[my_section]
                # 뉴스 요약
                for news_info in news_list3:
                    # 뉴스 본문이 10 문장 이하일 경우 결과 반환 x
                    # 요약하지 않고 본문에서 앞 3문장 사용
                    try:
                        snews_contents = summarize(news_info['news_contents'], word_count=40)
                    except:
                        snews_contents = None

                    if not snews_contents:
                        news_sentences = news_info['news_contents'].split('.')

                        if len(news_sentences) > 3:
                            snews_contents = '.'.join(news_sentences[:3])
                        else:
                            snews_contents = '.'.join(news_sentences)

                    news_info['snews_contents'] = snews_contents

                self.label2.append("첫번째 뉴스링크 \n"+news_list3[0]['news_url']+'\n\n뉴스 제목 \n'+str(news_list3[0]['title'])+'\n\n요약본 \n'+str(news_list3[0]['snews_contents']))
                self.label3.append("두번째 뉴스링크 \n"+news_list3[1]['news_url']+'\n\n뉴스 제목 \n'+str(news_list3[1]['title'])+'\n\n요약본 \n'+str(news_list3[1]['snews_contents']))
                self.label4.append("세번째 뉴스링크 \n"+news_list3[2]['news_url']+'\n\n뉴스 제목 \n'+str(news_list3[2]['title'])+'\n\n요약본 \n'+str(news_list3[2]['snews_contents']))

                self.label2.setFont(QFont("",11))
                self.label3.setFont(QFont("", 11))
                self.label4.setFont(QFont("", 11))
            except:
                news_no = QMessageBox.question(self, 'notification', '뉴스요약을 하지 못했습니다. 해당 숫자를 다시 입력해주세요.',
                                               QMessageBox.Yes)

        def main():

            newsSummarize(newsCr)

        main()


    def showModal(self):
        return super().exec_()
