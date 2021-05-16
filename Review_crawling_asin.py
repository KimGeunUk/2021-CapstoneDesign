from selenium import webdriver
from bs4 import BeautifulSoup
from tqdm.auto import tqdm
import time
import csv
import math

AMAZON_URL = 'https://www.amazon.com'
driver = webdriver.Chrome('C:/STUDY/chromedriver.exe')
driver.set_window_size(1280, 1024)
driver.implicitly_wait(5)           # 암묵적 대기

def review_crawling(product_asin, product):
    URL = f'{AMAZON_URL}/dp/product-reviews/{product_asin}?pageNumber={{}}'

    driver.get(URL)                 # URL 접속

    csvfile = open(f'./reviews/{product}/{product_asin.strip()}.csv', 'w', encoding="utf-8", newline="")

    writer = csv.DictWriter(csvfile, fieldnames=['title', 'star', 'content'], quoting=csv.QUOTE_ALL)
    writer.writeheader()

    # 총 리뷰 개수
    total_review = ''
    total_review_str = driver.find_element_by_xpath('//*[@id="filter-info-section"]/div/span').text
    total_reviews = total_review_str.split('|')
    # review_count_str[0]는 총 별점 개수
    for i in total_reviews[1]:
        if i.isdigit() == True:
            total_review += i

    start_page = 1
    end_page = (math.ceil(int(total_review) / 10)) - 1

    print(f'총 리뷰 개수는 : {total_review} 개 입니다. \nFrom the United States Review만 크롤링 합니다.')
    print(f'Start page : {start_page} | End page : {end_page}')
    print('진행중...')

    while True:
        try:
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            titles = soup.find_all('a', class_='review-title')
            contents = soup.find_all('span', class_='review-text-content')
            stars = soup.find_all('span', class_='a-icon-alt')
            next_page = soup.find_all('li', class_='a-last')

            for title, content, star in zip(titles, contents, stars):
                writer.writerow({'title' : title.get_text().strip(), 'star' : star.get_text().split(' ')[0], 'content' : content.get_text().strip()})

            driver.get(AMAZON_URL + next_page[0].find('a')['href'])
            start_page += 1
            time.sleep(1)
        except:
            print('이 제품 크롤링 완료')
            time.sleep(1)
            break

    csvfile.close()

print('크롤링을 시작합니다.')
i = 0
product = 'iphone'

with open(f'./reviews/{product}/{product}_asin.txt', 'r') as asinlist:
    for product_asin in asinlist.readlines():
        print(f'\nASIN #{i+1} : {product_asin.strip()}')
        review_crawling(product_asin, product)
        i += 1

    driver.quit()       #크롬 종료
    print(f'총 {i} 개의 제품을 크롤링 했습니다.')
