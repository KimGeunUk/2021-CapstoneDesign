import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

AMAZON_URL = 'https://www.amazon.com/'
driver = webdriver.Chrome('C:/STUDY/chromedriver.exe')
driver.set_window_size(1280, 1024)
sleep = 2

time.sleep(sleep)
# URL 접속
driver.get(AMAZON_URL)
# 저장 dataframe
index = []
df = pd.DataFrame(index, columns=['URL', 'star', 'content'])

# 리뷰 크롤링 함수
def review_crawling(product_asin):
    global df

    URL = f'{AMAZON_URL}/dp/product-reviews/{product_asin}?pageNumber={{}}'
    time.sleep(sleep)
    driver.get(URL)

    try:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        contents = soup.find_all('span', class_='review-text-content')
        stars = soup.find_all('span', class_='a-icon-alt')

        for content, star in zip(contents, stars):
            if ' ' in content.get_text().strip():
                continue
            else:
                df = df.append({'URL': URL, 'star': star.get_text().split(' ')[0][0], 'content': content.get_text().strip()}, ignore_index=True)

        time.sleep(1)
    except Exception as e:
        print('예외 발생 : ', e)
        time.sleep(1)

# Menu 창
time.sleep(sleep)
driver.find_element_by_id('nav-hamburger-menu').click()

# Menu See All
time.sleep(sleep)
driver.find_element_by_xpath('//*[@id="hmenu-content"]/ul[1]/li[11]/a[1]').click()

i = 6
while i != 13:
    try:
        # Men's Fashion : li[6] ~ Luggage : li[12]
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="hmenu-content"]/ul[1]/ul[1]/li[' + str(i) + ']/a').click()
    except Exception as e:
        print('큰 카테고리 문제')
        print(e)

    j = 3
    while True:
        print(i, j)
        try:
            # Men's Fashion - Clothing : li[3] ~
            time.sleep(sleep)
            driver.get(driver.find_element_by_xpath('//*[@id="hmenu-content"]/ul[' + str(i + 7) + ']/li[' + str(j) + ']/a').get_attribute('href'))
        except Exception as e:
            print('한 카테고리의 속 카테고리 크롤링 완료')
            i += 1
            time.sleep(sleep)
            break

        # asin값 리스트에 저장
        asin_list = []
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        content = soup.find_all('div', class_='s-asin')
        for asin in content:
            if asin.get('data-asin') == '':
                continue
            else:
                asin_list.append(asin.get('data-asin'))

        if len(asin_list) == 0:
            print('asin 값이 없는 속 카테고리 입니다.')
        else:
            # 리뷰 저장
            for k in range(10):
                review_crawling(asin_list[k])
            df = df.sample(frac=1).reset_index(drop=True)

        # 다음 카테고리
        j += 1

        try:
            time.sleep(2)
            # URL 접속
            driver.get(AMAZON_URL)
            # Menu 창
            time.sleep(sleep+1)
            driver.find_element_by_id('nav-hamburger-menu').click()
            # Menu See All
            time.sleep(sleep+1)
            driver.find_element_by_xpath('//*[@id="hmenu-content"]/ul[1]/li[11]/a[1]').click()
        except:
            df.to_csv('./reviews/test_shuffle2.csv', encoding='utf-8')

    df.to_csv('./reviews/test_shuffle' + str(i - 6) + '.csv', encoding='utf-8')
    index = []
    df = pd.DataFrame(index, columns=['URL', 'star', 'content'])

print('크롤링 끝!')
