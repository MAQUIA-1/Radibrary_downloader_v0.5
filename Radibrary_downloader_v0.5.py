import sys
import urllib.parse
#import time
#import re
#import datetime
import webbrowser
#from requests import get
import urllib.request
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from bs4 import BeautifulSoup
from radio_module import last_page_module ,url_list_module
from queston_pop_up import AuthDialog

form_class = uic.loadUiType('main.ui')[0]




class Main(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initSetting()
        self.initSignal()
        dlg = AuthDialog()
        dlg.exec_()



        # 초기 셋팅
    def initSetting(self):
        self.swordEdit.setFocus(True)
        self.download_button.setEnabled(False)
        self.statusBar().showMessage('제작: MAQUIA')



    #시그널
    def initSignal(self):
        self.setWindowTitle('Radibrary 다운로더 v0.5')
        self.swordEdit.returnPressed.connect(self.listWidget.clear)
        self.swordEdit.returnPressed.connect(self.extractWordStart)
        self.search_button.clicked.connect(self.listWidget.clear)
        self.search_button.clicked.connect(self.extractWordStart)
        self.download_button.clicked.connect(self.downloadButton)
        self.help_button.clicked.connect(self.question)
        self.location_button.clicked.connect(self.selectDownPath)
        self.homepage_button.clicked.connect(self.openHomepage)




    #검색결과 추출
    def extractWordStart(self):
        self.statusBar().showMessage('Radibrary 에서 검색결과 불러오는중... (응답이 없더라도 잠시 기다려주세요)')

        #검색어, 인코딩
        search = urllib.parse.quote_plus(self.swordEdit.text().strip())

        #마지막 페이지 모듈
        page_last = int(last_page_module(search))

        page_num = 1
        post_list = []
        url_list = []



        #검색 모듈 (제목프린트,리스트) (url프린트,리스트)
        while page_num < page_last + 1:
            url_list_module(post_list, url_list, search, page_num)
            QApplication.processEvents()
            page_num += 1


        #url 딕셔너리
        self.url_dic = dict(zip(post_list,url_list))

        for i in post_list:
            self.listWidget.addItem(i)

        print('검색완료!')
        print('\n----------------------------------------------------------------------------------\n')
        self.statusBar().showMessage('검색 완료')


    #다운로드 경로 지정
    def selectDownPath(self):
        fpath = QFileDialog.getExistingDirectory(self,'다운로드 경로')
        self.locaton_line.setText(fpath)

        down_dir = self.locaton_line.text().strip()

        self.download_button.setEnabled(True)
        if down_dir is None or down_dir == '' or not down_dir:
            self.download_button.setEnabled(False)


    #다운로드
    def downloadButton(self):

        self.statusBar().showMessage('다운로드 진행중... (응답이 없더라도 잠시 기다려주세요)')

        down_dir = self.locaton_line.text().strip()
        print(f'{down_dir} 에 저장')
        print('\n----------------------------------------------------------------------------------\n')
        self.selectedList = self.listWidget.selectedItems()

        post_selected_list = []
        url_selected_list = []

        for i in self.selectedList:

            print(i.text())
            post_selected_list.append(i.text())

        print('\n----------------------------------------------------------------------------------\n')
        print(f'\n{len(post_selected_list)} 개의 항목 선택.\n')
        print('\n----------------------------------------------------------------------------------\n')


        for i in post_selected_list:

            url_selected_list.append(self.url_dic.get(i))


        for url_i in url_selected_list:
            print(url_i, '에서 다운로드 링크 수집.....\n')
            html_2 = urllib.request.urlopen(url_i).read()
            soup_2 = BeautifulSoup(html_2, 'html.parser')

            download_link = soup_2.select('.moreless_content a')
            # 띄어쓰기가 하위클라스 전부 찾는거였음;;


            for i in download_link:
                print(i.get_text())
                print(i.attrs['href'], '\n')
                urllib.request.urlretrieve(i.attrs['href'], down_dir+'/'+i.get_text())  #다운로드
                QApplication.processEvents()

            print('\n----------------------------------------------------------------------------------\n')

        print('다운로드 완료!')
        print('\n----------------------------------------------------------------------------------\n')
        self.statusBar().showMessage('다운로드 완료!')


    #도움말
    def question(self):
        dlg = AuthDialog()
        dlg.exec_()


    #홈페이지 열기
    def openHomepage(self):
        webbrowser.open('https://radibrary.tistory.com/category')


if __name__ == "__main__" :

    app = QApplication(sys.argv)
    downloader = Main()
    downloader.show()
    app.exec_()