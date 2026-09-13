FROM python:3.12-slim

WORKDIR /app

# 先装依赖，利用缓存层
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 拷贝项目代码
COPY . .

# 平台（Zeabur/Render）会注入 PORT 环境变量，本地默认 8080
EXPOSE 8080
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]
