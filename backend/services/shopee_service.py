from backend.services.base_scraper import PlaywrightBaseService
import logging
import asyncio

logger = logging.getLogger(__name__)

class ShopeeService(PlaywrightBaseService):
    def __init__(self, headless: bool = True):
        super().__init__(headless=headless, session_file="sessions/shopee_session.json")
        self.login_url = "https://seller.shopee.tw/"

    async def login(self, username: str, password: str) -> bool:
        """登入蝦皮賣家中心"""
        p, browser, context, page = await self._init_browser()
        try:
            logger.info("前往蝦皮賣家中心登入頁面...")
            await page.goto(self.login_url)
            
            # TODO: 實作輸入帳號密碼邏輯 (須注意蝦皮的防爬蟲與簡訊認證)
            # await page.fill('input[name="username"]', username)
            # await page.fill('input[name="password"]', password)
            # await page.click('button[type="submit"]')
            # await page.wait_for_url("**/portal/dashboard**", timeout=10000)
            
            await self.save_session(context)
            return True
        except Exception as e:
            logger.error(f"蝦皮登入失敗: {e}")
            return False
        finally:
            await self.cleanup(p, browser)

    async def sync_products(self):
        """同步蝦皮賣家中心的商品"""
        p, browser, context, page = await self._init_browser()
        try:
            logger.info("蝦皮: 導覽至登入頁面...")
            await page.goto("https://seller.shopee.tw/")
            
            # 給予使用者 60 秒的充裕時間進行手動登入操作與圖形驗證
            logger.info("請在彈出的瀏覽器中手動完成蝦皮登入。等待中 (60秒)...")
            await page.wait_for_timeout(60000)
            
            logger.info("蝦皮: 再次確保導覽至商品管理頁面...")
            await page.goto("https://seller.shopee.tw/portal/product/list/all")
            
            # 等待商品清單容器出現
            await page.wait_for_selector('.product-list-container, .shopee-table', timeout=15000)
            await asyncio.sleep(2)
            
            logger.info("蝦皮: 正在擷取商品資料...")
            products = []
            # 找尋所有商品行
            items = await page.query_selector_all('.shopee-table-row, .product-item')
            for item in items:
                name_el = await item.query_selector('.product-name, .name')
                price_el = await item.query_selector('.product-price, .price')
                stock_el = await item.query_selector('.product-stock, .stock')
                sku_el = await item.query_selector('.product-sku, .sku')
                
                if name_el and price_el:
                    name = await name_el.inner_text()
                    price = await price_el.inner_text()
                    stock = await stock_el.inner_text() if stock_el else "0"
                    sku = await sku_el.inner_text() if sku_el else ""
                    
                    products.append({
                        "platform": "Shopee",
                        "sku": sku.strip(),
                        "name": name.strip(),
                        "price": price.replace(',', '').replace('$', '').strip(),
                        "stock": stock.strip()
                    })
            
            logger.info(f"蝦皮: 商品資料擷取完成，共 {len(products)} 筆")
            return products
        except Exception as e:
            logger.error(f"蝦皮商品同步發生問題: {e}")
            return []
        finally:
            await self.cleanup(p, browser)
        
    async def fetch_orders(self):
        """抓取蝦皮最新訂單"""
        p, browser, context, page = await self._init_browser()
        try:
            logger.info("蝦皮: 導覽至登入頁面...")
            await page.goto("https://seller.shopee.tw/")
            
            # 給予使用者 60 秒的充裕時間進行手動登入操作與圖形驗證
            logger.info("請在彈出的瀏覽器中手動完成蝦皮登入。等待中 (60秒)...")
            await page.wait_for_timeout(60000)
            
            logger.info("蝦皮: 再次確保導覽至訂單管理頁面...")
            await page.goto("https://seller.shopee.tw/portal/sale/order")
            
            await page.wait_for_selector('.order-list-container, .shopee-table', timeout=15000)
            await asyncio.sleep(2) 
            
            logger.info("蝦皮: 正在擷取訂單資料...")
            orders = []
            items = await page.query_selector_all('.order-item, .shopee-table-row')
            for item in items:
                order_id_el = await item.query_selector('.order-id')
                status_el = await item.query_selector('.order-status')
                amount_el = await item.query_selector('.order-amount')
                
                if order_id_el:
                    order_id = await order_id_el.inner_text()
                    status = await status_el.inner_text() if status_el else "未知"
                    amount = await amount_el.inner_text() if amount_el else "0"
                    
                    orders.append({
                        "platform": "Shopee",
                        "order_id": order_id.strip(),
                        "status": status.strip(),
                        "amount": amount.replace(',', '').replace('$', '').strip()
                    })
            
            logger.info(f"蝦皮: 訂單資料擷取完成，共 {len(orders)} 筆")
            return orders
        except Exception as e:
            logger.error(f"蝦皮訂單同步發生問題: {e}")
            return []
        finally:
            await self.cleanup(p, browser)
