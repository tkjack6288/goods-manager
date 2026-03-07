import logging
from playwright.async_api import async_playwright
from typing import Optional, Dict, Any
import os

logger = logging.getLogger(__name__)

class PlaywrightBaseService:
    def __init__(self, headless: bool = True, session_file: Optional[str] = None):
        self.headless = headless
        self.session_file = session_file
        
    async def _init_browser(self):
        """初始化瀏覽器並回傳 playwright, browser, context, page"""
        p = await async_playwright().start()
        browser = await p.chromium.launch(headless=self.headless)
        
        context_options: Dict[str, Any] = {
            'viewport': {'width': 1280, 'height': 800},
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
        
        session_file = self.session_file
        # 若有指定 session 檔案且存在，則載入 Cookie/Storage
        if session_file and os.path.exists(session_file):
            context_options['storage_state'] = session_file
            
        context = await browser.new_context(**context_options)
        page = await context.new_page()
        return p, browser, context, page
        
    async def save_session(self, context):
        """儲存當下的登入狀態"""
        session_file = self.session_file
        if session_file:
            # 確保目錄存在
            os.makedirs(os.path.dirname(session_file), exist_ok=True)
            await context.storage_state(path=session_file)
            logger.info(f"Session 狀態已儲存至 {session_file}")

    async def cleanup(self, p, browser):
        """關閉資源"""
        try:
            await browser.close()
            await p.stop()
        except Exception as e:
            logger.error(f"清理瀏覽器資源時發生錯誤: {e}")
