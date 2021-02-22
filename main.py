from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from urllib.parse import quote_plus

driver = webdriver.Chrome('chromedriver.exe')
SCROLL_PAUSE_SEC = 1.5
baseUrl = 'https://search.naver.com/search.naver?where=image&sm=tab_jum&query='


def set_search_object():
    plus_urls = input('검색어 입력(띄어쓰기로 구분): ')
    plus_url_list = plus_urls.split(' ')
    crawl_num = int(input('크롤링할 갯수 입력(100개 단위): 약 '))

    for p_url in plus_url_list:
        print(p_url)

        url = baseUrl + quote_plus(p_url)  # 한글 검색 자동 변환
        driver.get(url)
        scroll(crawl_num)
        get_images(p_url)


def scroll(crawl_num):
    scroll_num = int(crawl_num/70)
    last_height = driver.execute_script("return document.body.scrollHeight")
    for i in range (scroll_num):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_SEC)
        new_height = driver.execute_script("return document.body.scrollHeight")


def get_images(p_url):
    html = driver.page_source
    soup = bs(html, "html.parser")
    img = soup.find_all(class_='_image')
    n = 1
    print(len(img))
    # print(img)
    for i in img:
        img_url = i['src']
        if img_url[0] != 'h':
            img_url = i['data-lazy-src']
        print(n)
        try:
            with urlopen(img_url) as f:
                with open('./images/' + p_url + '_' + str(n) + '.jpg', 'wb') as h:  # w - write b - binary
                    img = f.read()
                    h.write(img)
        except:
            pass
        n += 1
    print(p_url, ' Image Crawling is done.')


if __name__ == '__main__':
    set_search_object()
    # scroll()
    # get_images()
