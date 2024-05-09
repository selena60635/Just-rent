import os, re
import shutil

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import json
import requests

def yahoo_car_crawler(url):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    driver.get(url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    spec_wrapper = soup.find('div', {'class': 'spec-wrapper'})
    if spec_wrapper is None:
        return None
    fields_dict = {
        'displacement': '排氣量',
        'body': '車身型式',
        'seat': '座位數',
        'door': '車門數',
        'car_length': '車長',
        'wheelbase': '軸距',
        'power_type': '動力型式'
    }

    # 將網頁的標題添加到車輛資訊中，並只取 '|' 前的部分
    title = soup.find('title').text
    car_name = title.split('|')[0].strip()
    info_dict = {
        'name': car_name.split()[0] + " " + " ".join(car_name.split()[2:]),
        'brand': car_name.split()[0],
        'model': " ".join(car_name.split()[2:]),
        'year': int(car_name.split()[1]),
        'price': 100  # 這裡不知道價錢要從何而來，先寫死做測試
    }
    save_images(soup, re.sub(r'\s+', '', car_name))
    for field_key, field in fields_dict.items():
        try:
            field_info = spec_wrapper.find('span', string=field)
        
            if field_info is not None:
                field_value = field_info.find_next_sibling('span').text
                numeric_value = re.search(r'\d+', field_value)  # 使用正則表達式提取數字
                if numeric_value is not None:
                    info_dict[field_key] = int(numeric_value.group())  # 若提取到數字，則轉換為整數型態
                else:
                    info_dict[field_key] = field_value  # 若未提取到數字，則使用原始值
            else:
                info_dict[field_key] = None

        except Exception as err:
            print(f"An error occurred '{field}': {err}")

    driver.quit()
    return info_dict

def save_images(soup, car_name):
    image_tags = soup.find_all('img', {'class': 'gabtn'})
    directory = os.path.join('app', 'static', 'cars-img', car_name)
    if not os.path.exists(directory):
        os.makedirs(directory)

    for i, img in enumerate(image_tags):
        if i >= 5:
            break
        img_url = img['src']
        response = requests.get(img_url, stream=True)

        if response.status_code == 200:
            response.raw.decode_content = True
            with open(directory + '/img_'+str(i)+'.jpg', 'wb') as f:
                shutil.copyfileobj(response.raw, f)




# 從 JSON 檔案讀取車輛列表
with open(os.path.join("app/script", "car_list.json"), "r") as file:
    car_list = json.load(file)

cars_info = []
for i, car in enumerate(car_list):
    # if i >= 1:
    #     break
    short_link = car['short_link']
    if short_link is not None:
        car_info = yahoo_car_crawler(short_link)
        if car_info is not None:
            cars_info.append(car_info)

# 將抓取的車輛資料存成 cars.json 檔案
with open(os.path.join("app/script", "cars.json"), "w") as file:
    json.dump(cars_info, file)
