from urllib.request import urlopen,Request
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os
ko_search = list(input("검색명:").split())        
total_time = time.time()
for i in range(len(ko_search)):
    ####################################################################################
    # 1. 웹 띄우기
    ####################################################################################
    ko_name = ko_search[i]
    print(ko_name + "의 데이터 수집 시작")

    # bing.com
    baseUrl = "https://www.bing.com/images/search?q="
    baseUrl2 = "&form=HDRSC2&first=1&scenario=ImageBasicHover"
    url = baseUrl + quote_plus(ko_name) + baseUrl2
    # headless을 활용하여 화면을 안띄움
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')

    driver = webdriver.Chrome(
            executable_path = "C:/Users/multicampus/chromedriver_win32/chromedriver.exe",
            chrome_options=options)
    
    driver.get(url)
    time.sleep(1)

    SCROLL_PAUSE_TIME = 1.0
    url_path = []
    ####################################################################################
    # 2. 이미지 url 수집
    ####################################################################################
    
    cnt = 0
    while cnt < 10:
        cnt +=1
        pageString = driver.page_source
        bsObj = BeautifulSoup(pageString, 'lxml')
        try:
            for line in bsObj.find_all(name='div', attrs={"class":"img_cont hoff"}):
                page = line.find(name="img")["src"]
                if page.find("data:image/jpeg") == -1:
                    url_path.append(page)
        
        except IndexError as ider:
            print("IndexError")
        
        last_height = driver.execute_script('return document.body.scrollHeight')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            else:
                last_height = new_height
                continue

        time.sleep(0.3)
        url_path = list(set(url_path))
    driver.close()

    url_path = list(set(url_path))
    print(ko_name,"의 이미지 갯수는 : ",len(url_path))
print(url_path)
print("총 걸린 시간 :", time.time() - total_time)  # 현재시각 - 시작시간 = 실행 시간)
    
