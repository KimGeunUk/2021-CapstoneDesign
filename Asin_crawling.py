from selenium import webdriver
from bs4 import BeautifulSoup
import os
import shutil

product = 'iphone'

def asin_crawling(product):
    URL = f'https://www.amazon.com/s?k={product}'
    driver = webdriver.Chrome('C:/STUDY/chromedriver.exe')
    driver.set_window_size(1280, 1024)
    # 암묵적 대기
    driver.implicitly_wait(5)
    driver.get(URL)

    if os.path.exists(f'./reviews/{product}'):
        shutil.rmtree(f'./reviews/{product}')   # 전체 디렉토리 트리 삭제
        os.mkdir(f'./reviews/{product}')        # keyword 디렉토리 재생성
    else:
        os.mkdir(f'./reviews/{product}')        # keyword 디렉토리 생성

    f = open(f'./reviews/{product}/{product}_asin.txt', 'w')

    while True:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        content = soup.find_all('div', class_='s-asin')
        next_bt = soup.find_all('li', class_='a-last')

        for asin in content:
            if asin.get('data-asin') == '':
                continue
            else:
                f.write(asin.get('data-asin') + '\n')
        try:
            driver.get(URL + next_bt[0].find('a')['href'])
        except:
            driver.close()          # driver 종료
            f.close()               # txt파일 쓰기 종료
            break

print(asin_crawling(product))
