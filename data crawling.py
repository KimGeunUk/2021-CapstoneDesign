from selenium import webdriver
from datetime import datetime
import csv
import time

URL = 'https://www.amazon.com/Centrum-Multivitamin-Multimineral-Supplement-Vitamin/dp/B00LEHDLRW/ref=sr_1_3?dchild=1&keywords=mutivitiam&qid=1615803864&sr=8-3'

driver = webdriver.Chrome('C:/STUDY/chromedriver.exe')
#암묵적 대기
driver.implicitly_wait(5)
#URL 접속
driver.get(URL)

#모든 REVIEW 페이지로 이동
driver.find_element_by_xpath('//*[@id="reviews-medley-footer"]/div[2]/a').click()

#REVIEW 추출
customer = []
reviews = []
titles = []
dates = []
stars = []
review_count = ''

#csv파일 쓰기 시작
f = open('REVIEW2.csv', 'w', encoding='utf-8')
w = csv.writer(f)

#제품 이름
name = driver.find_element_by_xpath('//*[@id="cm_cr-product_info"]/div/div[2]/div/div/div[2]/div[1]/h1').text
print('제품 이름은 :', name, '입니다.')
w.writerow(['제품명 : ' + name])

#리뷰 첫페이지
first_pages = 1
#리뷰 마지막페이지
last_pages = 20

#총 리뷰 개수
review_count_str = driver.find_element_by_xpath('//*[@id="filter-info-section"]/div/span').text
review_count_str = review_count_str.split('|')
#review_count_str[0]는 총 별점 개수
for i in review_count_str[1]:
    if i.isdigit() == True:
        review_count += i

print('총 리뷰 개수는 :', int(review_count), '개 입니다.')

while True:
    try:
        if first_pages == last_pages + 1:
            print('총', len(customer), '명의 리뷰를 크롤링 했습니다.')

            # csv파일 쓰기 종료
            f.close()
            # driver 종료
            driver.close()
            driver.quit()
            # 코딩 종료
            break
        else:
            if first_pages == 1:
                for i in range(1, 11):
                    customer.append(driver.find_element_by_xpath('//*[@id="cm_cr-review_list"]/div[' + str(i) + ']').get_attribute('id'))
            else:
                for i in range(2, 12):
                    customer.append(driver.find_element_by_xpath('//*[@id="cm_cr-review_list"]/div[' + str(i) + ']').get_attribute('id'))

            for i in range(first_pages*10 - 10, first_pages*10):
                #리뷰 내용
                reviews.append(driver.find_element_by_xpath('//*[@id="customer_review-' + customer[i] + '"]/div[4]/span/span').text)
                #리뷰 제목
                titles.append(driver.find_element_by_xpath('//*[@id="customer_review-' + customer[i] + '"]/div[2]/a[2]/span').text)
                #리뷰 날짜
                date = (driver.find_element_by_xpath('//*[@id="customer_review-' + customer[i] + '"]/span').text).split(' ')
                dates.append(date[-1] + '-' + date[-3] + '-' + date[-2])
                #리뷰 별점 (icon이라 text가 안보임)
                star = driver.find_element_by_xpath('//*[@id="customer_review-' + customer[i] + '"]/div[2]/a[1]/i/span').get_attribute('textContent')
                stars.append('평점은 ' + star[0] + '점 입니다.')

            for i in range(first_pages*10 - 10, first_pages*10):
                w.writerow([i+1, '\n', stars[i], '\n', titles[i], '\n', dates[i], '\n', reviews[i]])

        driver.find_element_by_xpath('//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a').click()
        #시간 두기
        time.sleep(3)

        print('현재 페이지는 ', first_pages, '입니다.')
        first_pages += 1

    except Exception as e:
        print("최대 페이지 입니다. 에러 : ", e)
        print('총', len(customer), '명의 리뷰를 크롤링 했습니다.')

        #csv파일 쓰기 종료
        f.close()
        #driver 종료
        driver.close()
        driver.quit()
        #코딩 종료
        break