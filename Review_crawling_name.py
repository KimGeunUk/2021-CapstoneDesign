from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import csv
import time

item = 'multivitamin'

def item_crawling(item, item_num):
    AMAZON_URL = 'https://www.amazon.com/'
    driver = webdriver.Chrome('C:/STUDY/chromedriver.exe')
    driver.set_window_size(1280, 1024)
    # 암묵적 대기
    driver.implicitly_wait(5)
    # URL 접속
    driver.get(AMAZON_URL)

    search_item = driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
    search_item.send_keys(item)
    driver.find_element_by_xpath('//*[@id="nav-search-submit-button"]').click()
    time.sleep(3)

    if item_num > 45:
        driver.close()
        driver.quit()
        return 0

    try:
        driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[2]/div[' + str(item_num) + ']/div/span/div/div/span/a/div/img').click()
    except:
        driver.find_element_by_xpath('//*[@id="search"]/div[1]/div/div[1]/div/span[3]/div[2]/div[' + str(item_num) + ']/div/span/div/div/span/a/div/img').click()
        URL = driver.current_url
    else:
        URL = driver.current_url

    driver.close()
    driver.quit()

    review_crawling(URL, item_num)

    return 0

def review_crawling(URL, item_num):
    driver = webdriver.Chrome('C:/STUDY/chromedriver.exe')
    driver.set_window_size(1280, 1024)
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

    #REVIEW 개수
    count = 0
    cnt = 10

    #csv파일 쓰기 시작
    f = open('REVIEW' + str(item_num - 2) + '.csv', 'w', encoding='utf-8')
    w = csv.writer(f)

    #제품 이름
    name = driver.find_element_by_xpath('//*[@id="cm_cr-product_info"]/div/div[2]/div/div/div[2]/div[1]/h1').text
    print('제품 이름은 :', name, '입니다.')
    #w.writerow(['제품명 : ' + name])
    w.writerow(['num', 'star', 'title', 'date', 'review'])

    #총 리뷰 개수
    review_count_str = driver.find_element_by_xpath('//*[@id="filter-info-section"]/div/span').text
    review_count_str = review_count_str.split('|')
    #review_count_str[0]는 총 별점 개수
    for i in review_count_str[1]:
        if i.isdigit() == True:
            review_count += i

    print('총 리뷰 개수는 :', int(review_count), '개 입니다. 미국 리뷰만 크롤링 합니다.')

    #리뷰 첫페이지
    first_pages = 1
    #리뷰 마지막페이지
    last_pages = int(review_count) / 10

    while True:
        if first_pages == last_pages + 1:
            print('총', count, '명의 리뷰를 크롤링 했습니다.')

            # csv파일 쓰기 종료
            f.close()
            # driver 종료
            driver.close()
            driver.quit()
            # 다음 아이템
            item_num += 1
            # 코딩 종료
            break

        else:
            #리뷰 ID 추출
            for i in range(2, 12):
                try:
                    #다른 나라 리뷰 페이지 발견
                    if driver.find_element_by_xpath('//*[@id="cm_cr-review_list"]/div[' + str(i) + ']').get_attribute('class') == 'a-divider a-divider-section':
                        cnt = i - 2
                        break
                    else:
                        if first_pages == 1:
                            customer.append(driver.find_element_by_xpath('//*[@id="cm_cr-review_list"]/div[' + str(i-1) + ']').get_attribute('id'))
                        else:
                            customer.append(driver.find_element_by_xpath('//*[@id="cm_cr-review_list"]/div[' + str(i) + ']').get_attribute('id'))
                except NoSuchElementException:
                    cnt = i - 3
                    break

            #리뷰 내용, 제목, 날짜, 별점 추출
            for i in range(0, cnt):
                try:
                    reviews.append(driver.find_element_by_xpath('//*[@id="customer_review-' + customer[i] + '"]/div[4]/span/span').text)
                except NoSuchElementException:
                    reviews.append('image review')
                titles.append(driver.find_element_by_xpath('//*[@id="customer_review-' + customer[i] + '"]/div[2]/a[2]/span').text)
                date = (driver.find_element_by_xpath('//*[@id="customer_review-' + customer[i] + '"]/span').text).split(' ')
                dates.append(date[-1] + '-' + date[-3] + '-' + date[-2])
                star = driver.find_element_by_xpath('//*[@id="customer_review-' + customer[i] + '"]/div[2]/a[1]/i/span').get_attribute('textContent')
                stars.append(star[0] + ' stars')

        #csv 파일에 리뷰 쓰기
        for i in range(0, cnt):
            count += 1
            w.writerow([count, stars[i], titles[i], dates[i], reviews[i]])

        #리스트 초기화
        customer = []
        reviews = []
        titles = []
        dates = []
        stars = []

        try:
            print('현재 페이지는 ', first_pages, '입니다.')
            if cnt < 10:
                raise Exception
            else:
                driver.find_element_by_xpath('//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a').click()
        except:
            print('더 이상 페이지 또는 리뷰가 없습니다.')
            print('총', count, '명의 리뷰를 크롤링 했습니다.')

            # csv파일 쓰기 종료
            f.close()
            # driver 종료
            driver.close()
            driver.quit()
            # 다음 아이템
            item_num += 1
            # 코딩 종료
            break

        #시간 두기
        time.sleep(2)
        #다음 페이지
        first_pages += 1

    return item_crawling(item, item_num)

print(item_crawling(item, 5))