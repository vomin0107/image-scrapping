from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from urllib.parse import quote_plus

url = 'http://bl-h5-as.robotbona.com/'
idpw = 'danhui1639'
driver = webdriver.Chrome('chromedriver.exe')
img = ''
url = ''
plusUrl = ''
SCROLL_PAUSE_SEC = 1.5
crawl_num = 0

baseUrl = 'https://search.naver.com/search.naver?where=image&sm=tab_jum&query='


def set_search_object():
    global crawl_num, url, plusUrl
    plusUrl = input('검색어 입력: ')
    crawl_num = int(input('크롤링할 갯수 입력(100개 단위): 약 '))

    url = baseUrl + quote_plus(plusUrl)  # 한글 검색 자동 변환
    driver.get(url)


def scroll():
    global crawl_num
    scroll_num = int(crawl_num/70)
    last_height = driver.execute_script("return document.body.scrollHeight")
    for i in range (scroll_num):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_SEC)
        new_height = driver.execute_script("return document.body.scrollHeight")


def get_images():
    global plusUrl
    html = driver.page_source
    soup = bs(html, "html.parser")
    img = soup.find_all(class_='_image')
    n = 1
    print(len(img))
    # print(img)
    for i in img:
        imgUrl = i['src']
        if imgUrl[0] != 'h':
            imgUrl = i['data-lazy-src']
        print(n)
        try:
            with urlopen(imgUrl) as f:
                with open('./images/' + plusUrl + '_' + str(n) + '.jpg', 'wb') as h:  # w - write b - binary
                    img = f.read()
                    h.write(img)
        except:
            pass
        n += 1
        # if n > crawl_num:
        #     break
    print('Image Crawling is done.')


if __name__ == '__main__':
    set_search_object()
    scroll()
    get_images()
