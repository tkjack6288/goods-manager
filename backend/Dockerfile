FROM python:3.11-slim

WORKDIR /app

# 安裝系統相依套件與 Playwright 依賴
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# 安裝 dependencies
COPY pyproject.toml .
RUN pip install uv
RUN uv pip install --system -e .

# 安裝 Playwright 瀏覽器
RUN python -m playwright install chromium
RUN python -m playwright install-deps chromium

COPY . .

# 啟動命令 (不使用 reload，且綁定在 PORT 環境變數)
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
