
from PyQt5.QtWidgets import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import os
from email.mime.base import MIMEBase

class SubWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('메일전송하기')
        self.setGeometry(800, 200, 400, 600)
        layout = QVBoxLayout()
        layout.addStretch(1)
        edit = QLineEdit()
        font = edit.font()
        font.setPointSize(20)

        #수신 email
        self.label1 = QLabel("수신email",self)
        self.label1.move(10,0)
        self.label1.resize(100, 30)
        self.line1 = QLineEdit(self)
        self.line1.move(70, 0)
        self.line1.resize(100, 25)

        #발신 email
        self.label2 = QLabel("내email", self)
        self.label2.move(15, 30)
        self.label2.resize(100, 30)
        self.line2 = QLineEdit(self)
        self.line2.move(70, 30)
        self.line2.resize(100, 25)

        #pw
        self.label3 = QLabel("pwd", self)
        self.label3.move(25, 60)
        self.label3.resize(100, 30)
        self.line3 = QLineEdit(self)
        self.line3.setEchoMode(QLineEdit.Password)
        self.line3.move(70, 60)
        self.line3.resize(100, 25)

        #title
        self.label4 = QLabel("메일제목", self)
        self.label4.move(10, 90)
        self.label4.resize(100, 30)
        self.line4 = QLineEdit(self)
        self.line4.move(70, 90)
        self.line4.resize(200, 25)

        #text
        self.label5 = QLabel("메일내용", self)
        self.label5.move(10, 120)
        self.label5.resize(100, 30)
        self.line5 = QLineEdit(self)
        self.line5.move(70, 120)
        self.line5.resize(300, 250)

        #버튼 클릭
        self.btnRun = QPushButton("메일전송", self)  # 버튼 텍스트
        self.btnRun.move(120, 380)  # 버튼 위치
        self.btnRun.resize(150, 30)
        self.btnRun.clicked.connect(self.btnRun_clicked)

        #첨부파일
        self.btnFile = QPushButton("파일선택",self)
        self.btnFile.clicked.connect(self.btnFile_clicked)
        self.lineFile = QLineEdit(self)
        layout.addWidget(self.btnFile)
        layout.addWidget(self.lineFile)
        self.setLayout(layout)

    def btnFile_clicked(self):
        fname = QFileDialog.getOpenFileName(self)
        self.lineFile.setText(fname[0])


    def btnRun_clicked(self):
        receive = self.line1.text()
        toss = self.line2.text()
        pwd = self.line3.text()
        title = self.line4.text()
        text = self.line5.text()
        file = self.lineFile.text()

        def Mailsend(receive,toss,pwd,title,text,file):
            try:
                toAddr = receive #받는사람
                email = toss  # 보내는사람
                pw = pwd  # 비밀번호
                tlt = title
                openfile = file
                maintext = text
                smtp = smtplib.SMTP('smtp.gmail.com', 587)  # 587서버의 모든 번호
                smtp.ehlo()
                smtp.starttls()  # tls방식으로 접속, 포트번호 587
                smtp.login(email, pw)  # 로그인

                #title
                msg = MIMEMultipart()
                msg['Subject'] = tlt


                #text
                part = MIMEText(maintext,'html','utf-8')
                msg.attach(part)
                attachments = [
                    os.path.join(os.getcwd(), 'storage', openfile)
                ]

                for attachment in attachments:
                    attach_binary = MIMEBase("application", "octect-stream")
                    binary = open(attachment, "rb").read()  # read file to bytes
                    attach_binary.set_payload(binary)
                    encoders.encode_base64(attach_binary)  # Content-Transfer-Encoding: base64
                    filename = os.path.basename(attachment)
                    attach_binary.add_header("Content-Disposition", 'attachment', filename=('utf-8', '', filename))
                    msg.attach(attach_binary)
                smtp.sendmail(email,toAddr, msg.as_string())

                mail_yes = QMessageBox.question(self, 'notification', '메일이 전송되었습니다.',
                                             QMessageBox.Yes)
            except :
                mail_no = QMessageBox.question(self, 'notification', '메일 전송에 실패 했습니다.\n다시 입력해주세요.',
                                             QMessageBox.Yes)

        def main():
            # query = input("검색어 입력: ")  # 네이버, 부동산...
            # info_main = input("=" * 50  + "\n" + " 뉴스요약 성공 Enter를 눌러주세요." + "\n" + "=" * 50)
            Mailsend(receive,toss,pwd,title,text,file)

        main()
    def showModal(self):
        return super().exec_()

