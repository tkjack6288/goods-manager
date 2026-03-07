FROM node:20-alpine AS base

# 安裝 libc6-compat 避免 Next.js build 時可能的缺失
RUN apk add --no-cache libc6-compat
WORKDIR /app

# 安裝 dependencies
COPY package.json package-lock.json ./
RUN npm ci

# 複製原始碼並建置
COPY . .
# 這裡請確保 .env 檔若有關鍵變數，要在建置時能讀到或使用 run 階段帶入
RUN npm run build

# 啟動應用程式
CMD ["npm", "run", "start"]
