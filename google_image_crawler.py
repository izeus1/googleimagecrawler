#-*- coding:utf-8 -*-

import os
import time
import csv
from urllib.request import Request, urlopen
import urllib.request
from selenium import webdriver

from bs4 import BeautifulSoup

#   구글 이미지 검색 함수
def crawling_google_images():

    #   구글은 크롤러로 진입시 403 에러가 뜨므로, urllib에 오프너로 헤더를 주입해줘야 함.
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)

    with open("__result__/practice.csv", 'r',
              encoding='UTF8') as link_table:
        reader = csv.reader(link_table)

        #   헤더가 있기때문에 다음 줄부터 시작
        next(reader)

        #   순환하면서 읽어들임.
        for line in reader:
            #   어트랙션 이름
            name = line[1]

            #   검색할 키워드
            keyword = name

            #   구글 이미지 검색 주소. 튜플을 이용하여 키워드를 직접 집어넣는다.
            #   tbm=isch 이미지 서치
            #   tbs=isz%3Al 큰 이미지
            #   q=keyword 검색어
            url = "https://www.google.com/search?tbm=isch&tbs=isz%" + "3Al&q=%s" % keyword

            #   셀레늄 경로
            wd = webdriver.Chrome('D:/JAVA_BIGDATA/chromedriver_win32/chromedriver.exe')

            #   셀레늄을 실행시키고 위의 키워드가 포함된 웹페이지 주소로 이동
            wd.get(url)
            time.sleep(3)
            html = wd.page_source

            #   BeautifulSoup를 이용하여 해당 테이블을 객체로 만듦
            bs = BeautifulSoup(html, 'html.parser')

            #   구글 이미지페이지에서 맨 앞에 표시되는 이미지 링크를 가져옴
            tag_rg = bs.find('div', attrs={'id' : 'rg'})
            tags_link = tag_rg.find_all('a', attrs={'class': 'rg_l'})

            for index, tag_link in enumerate(tags_link[0:3]):
                img_src = tag_link.get('href')

                #   해당 이미지는 해상도가 낮기 때문에 다시 한번 그 링크를 타서 이미지를 가져오기 위해 링크를 가져온다.
                url = "https://www.google.com" + img_src

                #   셀레늄으로 해당 링크 이동
                wd.get(url)
                time.sleep(3)
                html = wd.page_source

                bs = BeautifulSoup(html, 'html.parser')
                tags_images = bs.find_all('img', attrs={'class' : 'irc_mi'})
                img = tags_images[1].get('src')

                #   해당 키워드로 경로 생성
                if not (os.path.isdir("img/" + keyword)):
                    os.makedirs(os.path.join("img/" + keyword))

                #   이미지 저장
                #   경로 맨앞에 /가 있으면 맨위 루트 폴더, C드라이브에 저장되므로 주의!!
                urllib.request.urlretrieve(img, "img/%s/%d.jpg" % (keyword, index))


#   크롤링 함수 실행 코드
if __name__ == "__main__":
    #   어트랙션 정보 크롤링
    crawling_google_images()