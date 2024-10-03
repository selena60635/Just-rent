# 使用 Python 3.9 slim 作為基礎映像
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝相依套件
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案的所有檔案到容器
COPY . .

# 暴露 Gunicorn 使用的 8000 端口
EXPOSE 8000

# 使用 Gunicorn 啟動 Flask 應用
CMD ["gunicorn", "-b", "0.0.0.0:8000", "just_rent:app"]
