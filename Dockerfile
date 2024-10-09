
# FROM python:3.9-slim
# WORKDIR /app
# # ADD . /app
# COPY . /app
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt
# CMD ["gunicorn", "-b", "0.0.0.0:8000", "just_rent:app"]
FROM python:3.9-slim

# # 設定工作目錄
WORKDIR /my_app

# # 將需求文件複製到容器中
COPY requirements.txt .

# # 安裝套件
RUN pip install --no-cache-dir -r requirements.txt

# # 將所有應用程式文件複製到工作目錄
COPY . .


# # # 應用程式運行的端口
EXPOSE 8000


# # 使用 Gunicorn 啟動 Flask 應用
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "just_rent:app"]
CMD ["gunicorn", "-b", "0.0.0.0:8000", "just_rent:app"]
