import requests
from bs4 import BeautifulSoup
import json, os

def sscar_crawler(url, max_pages=6):
    result = []
    # 處理分頁
    for page in range(1, max_pages+1):
        page_url = f"{url}/page/{page}/"
        response = requests.get(page_url)
        if response.status_code != 200:
            break
        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.find_all('div', class_='product-small')
        for product in products:
            name = product.find('a', class_='woocommerce-LoopProduct-link').text
            url = product.find('a', class_='woocommerce-LoopProduct-link')['href']
            # 檢查是否已經存在相同的車輛，如果是則跳過
            if not any(car['url'] == url for car in result):
                result.append({'name': name, 'url': url})
    return result

def get_yahoo_link(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        h4_elements = soup.find_all('h4')
        if h4_elements:
            link_element = h4_elements[1].find('a')
            if link_element:
                link = link_element['href']
                return link
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


url = "https://sscars.com.tw/car/"
car_list = sscar_crawler(url)

for car in car_list:
    url = car['url']
    if url is not None:
        car['short_link'] = get_yahoo_link(url)
        
# 將車輛列表轉換為 JSON 格式的字串
car_list_json = json.dumps(car_list)

# 將 JSON 字串寫入檔案
with open(os.path.join("app/script", "car_list.json"), "w") as file:
    file.write(car_list_json)



