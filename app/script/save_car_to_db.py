# import json, os
# from sqlalchemy import create_engine, text
# from sqlalchemy.orm import sessionmaker
# import sys
# sys.path.append('/mnt/d/媜/code/饅頭計畫/just-rent')

# from app.models import Car
# from config import Config


# # 建立資料庫連線
# engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)


# # 建立 Session 類別
# Session = sessionmaker(bind=engine)

# # 建立 Session 物件
# session = Session()

# # 從文件中載入 JSON 數據
# with open(os.path.join("app/script", "cars.json"), 'r') as f:
#     data = json.load(f)

# # 將 JSON 數據轉換為 Car 物件並添加到 session
# for item in data:
#     car_spec = Car(
#         name=item['name'], 
#         seat=item['seat'],
#         door=item['door'],
#         body=item['body'],
#         displacement=item['displacement'],
#         car_length=item['car_length'],
#         wheelbase=item['wheelbase'],
#         power_type=item['power_type'],
#         brand=item['brand'],
#         model=item['model'],
#         year=item['year'],
#         # price=item['price'],
#     )
#     session.add(car_spec)

# # 提交 session
# session.commit()

# # 關閉 session
# session.close()
import json, os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import sys

# 動態設置路徑，根據環境變數選擇不同的根路徑
if os.getenv('ENVIRONMENT') == 'container':
    base_path = '/my_app'  # 容器內的路徑
else:
    base_path = '/mnt/d/媜/code/饅頭計畫/just-rent'  # 開發環境的路徑

sys.path.append(base_path)

from app.models import Car
from config import Config

# 建立資料庫連線
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)

# 建立 Session 類別
Session = sessionmaker(bind=engine)

# 建立 Session 物件
session = Session()

# 從文件中載入 JSON 數據
json_file_path = os.path.join(base_path, "app/script", "cars.json")
with open(json_file_path, 'r') as f:
    data = json.load(f)

# 將 JSON 數據轉換為 Car 物件並添加到 session
for item in data:
    car_spec = Car(
        name=item['name'], 
        seat=item['seat'],
        door=item['door'],
        body=item['body'],
        displacement=item['displacement'],
        car_length=item['car_length'],
        wheelbase=item['wheelbase'],
        power_type=item['power_type'],
        brand=item['brand'],
        model=item['model'],
        year=item['year'],
        # price=item['price'],
    )
    session.add(car_spec)

# 提交 session
session.commit()

# 關閉 session
session.close()
