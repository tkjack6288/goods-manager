from backend.services.base_scraper import PlaywrightBaseService
import logging
import asyncio

logger = logging.getLogger(__name__)

class MomoService(PlaywrightBaseService):
    def __init__(self, headless: bool = True):
        # 假設將儲存 cookie 的檔案放在相對目錄的 sessions 資料夾下
        super().__init__(headless=headless, session_file="sessions/momo_session.json")
        self.login_url = "https://scm.momoshop.com.tw/manage/login.jsp"

    async def login(self, username: str, password: str) -> bool:
        """登入 Momo SCM 生態系"""
        p, browser, context, page = await self._init_browser()
        try:
            logger.info("正在準備前往 Momo SCM 登入頁面...")
            await page.goto(self.login_url)
            
            # TODO: 實作輸入帳號密碼並通過圖形驗證碼/防機器人機制的邏輯
            # await page.fill('input[name="userId"]', username)
            # await page.fill('input[name="password"]', password)
            # 處理驗證碼... 
            # await page.click('button[type="submit"]')
            # await page.wait_for_url("**/manage/index**", timeout=10000)
            
            # 若登入成功，儲存 session
            await self.save_session(context)
            return True
        except Exception as e:
            logger.error(f"Momo 登入失敗: {e}")
            return False
        finally:
            await self.cleanup(p, browser)

    async def sync_products(self):
        """抓取與同步 Momo 平台上的商品"""
        p, browser, context, page = await self._init_browser()
        try:
            logger.info("Momo: 開始導覽至登入頁面...")
            await page.goto("https://scm.momoshop.com.tw/manage/login.jsp") 
            await asyncio.sleep(2)
            
            # 給予使用者 60 秒的充裕時間進行手動登入操作與圖形驗證
            logger.info("請在彈出的瀏覽器中手動完成 Momo 登入。等待中 (60秒)...")
            await page.wait_for_timeout(60000)
            
            # 點選左側選單進入商品管理
            # 若選單在 iframe 內，可能需使用 page.frame_locator
            await page.click('text="商品頁籤"', timeout=10000)
            await asyncio.sleep(1)
            await page.click('text="商品管理"')
            await asyncio.sleep(1)
            await page.click('text="B101 新增/管理商品"')
            
            # 等待資料表格出現
            logger.info("Momo: 正在擷取商品資料...")
            await page.wait_for_selector('table.grid-table, table.data-table', timeout=15000)
            
            products = []
            # 模擬分析表格 tr 
            rows = await page.query_selector_all('table.grid-table tbody tr, table.data-table tbody tr')
            for row in rows:
                cols = await row.query_selector_all('td')
                if len(cols) >= 4:
                    name = await cols[1].inner_text()
                    price_text = await cols[2].inner_text()
                    stock_text = await cols[3].inner_text()
                    
                    products.append({
                        "platform": "Momo",
                        "name": name.strip(),
                        "price": price_text.replace(',', '').replace('$', '').strip(),
                        "stock": stock_text.strip()
                    })
                    
            logger.info(f"Momo: 商品資料擷取完成，共 {len(products)} 筆")
            return products
        except Exception as e:
            logger.error(f"Momo 商品同步發生問題: {e}")
            return []
        finally:
            await self.cleanup(p, browser)
        
    async def fetch_orders(self):
        """抓取 Momo 最新訂單"""
        p, browser, context, page = await self._init_browser()
        try:
            logger.info("Momo: 開始導覽至登入頁面...")
            await page.goto("https://scm.momoshop.com.tw/manage/login.jsp")
            await asyncio.sleep(2)
            
            # 給予使用者 60 秒的充裕時間進行手動登入操作與圖形驗證
            logger.info("請在彈出的瀏覽器中手動完成 Momo 登入。等待中 (60秒)...")
            await page.wait_for_timeout(60000)
            
            await page.click('text="訂單管理"')
            await asyncio.sleep(1)
            await page.click('text="出貨處理"')
            
            logger.info("Momo: 正在擷取訂單資料...")
            await page.wait_for_selector('table.order-table', timeout=15000)
            
            orders = []
            rows = await page.query_selector_all('table.order-table tbody tr')
            for row in rows:
                cols = await row.query_selector_all('td')
                if len(cols) >= 5:
                    order_id = await cols[0].inner_text()
                    status = await cols[1].inner_text()
                    customer = await cols[2].inner_text()
                    amount = await cols[3].inner_text()
                    
                    orders.append({
                        "platform": "Momo",
                        "order_id": order_id.strip(),
                        "status": status.strip(),
                        "customer": customer.strip(),
                        "amount": amount.replace(',', '').replace('$', '').strip()
                    })
                    
            logger.info(f"Momo: 訂單資料擷取完成，共 {len(orders)} 筆")
            return orders
        except Exception as e:
            logger.error(f"Momo 訂單同步發生問題: {e}")
            return []
        finally:
            await self.cleanup(p, browser)
