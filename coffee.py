import requests

import time ##크롤링시 지연시간
from bs4 import BeautifulSoup
from selenium import webdriver
from pprint import pprint
import pandas as pd

import pymongo
import certifi
from pymongo import MongoClient

ca = certifi.where()

## ssori db
client = MongoClient('mongodb+srv://test:sparta@cluster0.2ftmiuw.mongodb.net/?retryWrites=true&w=majority', tlsCaFile=ca)
db = client.dbsparta

## 8조 db
# client = MongoClient('mongodb+srv://test:sparta@cluster0.ffudy0q.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCaFile=ca)
# db = client.coffeeduckhu

# webdriver 실행
chromedriver_dir = r'/Users/ssori/Desktop/chromedriver.exe'
driver = webdriver.Chrome(chromedriver_dir)

# page 접근
driver.get('https://www.starbucks.co.kr/menu/drink_list.do')

# html source 추출
html_source = driver.page_source

# BS로 html parsing
soup = BeautifulSoup(html_source, 'html.parser')

# 원하는 항목의 데이터만 추출
products = soup.select('.product_list dd a')

# 결과 확인
# pprint(products)

# 제품 이름, 코드 추출
prod_cd = [[product['prod'], product.find('img')['alt'], product.find('img')['src']] for product in products]

# 결과 확인
# pprint(prod_cd)

# result를 담을 빈 List 생성
result = []

# 제품별로 for loop
for prod in prod_cd:
    try:
        container = dict()
        cd = prod[0]
        name = prod[1]
        src = prod[2]
        driver.get("https://www.starbucks.co.kr/menu/drink_view.do?product_cd={prod_cd}".format(prod_cd=cd))
        html_source = driver.page_source
        soup = BeautifulSoup(html_source, 'html.parser')

        desc = soup.select_one('.myAssignZone p').get_text()

        # 용량 정보
        volume = soup.select_one('.product_info_head #product_info01').get_text()

        # 제품 영양정보
        kcal = soup.select_one('.product_info_content .kcal dd').get_text()
        sat_FAT = soup.select_one('.product_info_content .sat_FAT dd').get_text()
        protein = soup.select_one('.product_info_content .protein dd').get_text()
        fat = soup.select_one('.product_info_content .fat dd').get_text()
        trans_FAT = soup.select_one('.product_info_content .trans_FAT dd').get_text()
        protein = soup.select_one('.product_info_content .protein dd').get_text()
        sodium = soup.select_one('.product_info_content .sodium dd').get_text()
        sugars = soup.select_one('.product_info_content .sugars dd').get_text()
        caffeine = soup.select_one('.product_info_content .caffeine dd').get_text()
        cholesterol = soup.select_one('.product_info_content .cholesterol dd').get_text()
        chabo = soup.select_one('.product_info_content .chabo dd').get_text()

        # 필요한 정보
        ## 유니크 id 값을 db length + 1 로 지정 db.{소분류} 넣어줘야함
        count = list(db.nonCoffeeCheck.find({}, {'_id': False}))
        num = len(count) + 1
        container['coffee_id'] = num
        container['cafe'] = 'starbucks'
        container['coffee_name'] = name
        container['coffee_image'] = src
        container['coffee_desc'] = desc
        checkCoffee = int(caffeine) >= 100
        if checkCoffee:
            container['type'] = 'coffee'
        else:
            container['type'] = 'non-coffee'

        container['caffeine'] = caffeine + 'mg'
        container['calorie'] = kcal+'kcal'
        container['protein'] = protein + 'g'
        container['salt'] = sodium+'mg'
        container['saturated_fat'] = trans_FAT+'g'
        container['sugars'] = sugars+'g'

        result.append(container)
        print(container)

        db.nonCoffeeCheck.insert_one(container)
        # 트래픽 조절을 위해 2초간 pause
        time.sleep(2)
    except:
        print('error')
    finally:
        pprint(result)
        # DataFrame으로 변환
        df = pd.DataFrame(result)

        # csv파일로 저장
        df.to_csv('./starbucks.csv', index=False)

        # 데이터 확인
        df



