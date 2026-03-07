import sys
import os

# 將專案根目錄 (goods-manager) 加入 Python 系統路徑中
# 這樣 Python 就能夠正確識別並匯入 `backend` 作為模組
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import uvicorn

if __name__ == "__main__":
    # 使用正確的模組路徑啟動 FastAPI
    # ⚠️ 注意：Windows 下啟動 Playwright subprocess 必須關閉 reload=True 
    # 否則 Uvicorn 會強制覆寫 event loop 導致 NotImplementedError
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000)
