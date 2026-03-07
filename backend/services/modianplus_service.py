from backend.services.base_scraper import PlaywrightBaseService
import logging
import asyncio

logger = logging.getLogger(__name__)

class ModianPlusService(PlaywrightBaseService):
    def __init__(self, headless: bool = True):
        super().__init__(headless=headless, session_file="sessions/modian_session.json")
        self.login_url = "https://3p.momo.com.tw/" # mo店+ 商家後台登入網址

    async def login(self, username: str, password: str) -> bool:
        """登入 mo店+ 商家後台"""
        p, browser, context, page = await self._init_browser()
        try:
            logger.info("前往 mo店+ 後台登入頁面...")
            await page.goto(self.login_url)
            
            # TODO: 實作輸入帳號密碼邏輯
            # await page.fill('input[name="account"]', username)
            # await page.fill('input[name="password"]', password)
            # await page.click('button[type="submit"]')
            # await page.wait_for_url("**/admin/dashboard**", timeout=10000)
            
            await self.save_session(context)
            return True
        except Exception as e:
            logger.error(f"mo店+ 登入失敗: {e}")
            return False
        finally:
            await self.cleanup(p, browser)

    async def sync_products(self):
        """同步 mo店+ 平台上的商品"""
        p, browser, context, page = await self._init_browser()
        try:
            logger.info("mo店+: 導覽至登入頁面...")
            await page.goto("https://3p.momo.com.tw/")
            
            # 給予使用者 60 秒的充裕時間進行手動登入操作與圖形驗證
            logger.info("請在彈出的瀏覽器中手動完成 mo店+ 登入。等待中 (60秒)...")
            await page.wait_for_timeout(60000)
            
            # 等待商品列表加載
            await page.wait_for_selector('.product-list, table.el-table__body', timeout=15000)
            await asyncio.sleep(2)
            
            logger.info("mo店+: 正在擷取商品資料...")
            products = []
            rows = await page.query_selector_all('tr.el-table__row, tr.product-row')
            for row in rows:
                cols = await row.query_selector_all('td')
                if len(cols) >= 4:
                    name = await cols[1].inner_text()
                    price = await cols[2].inner_text()
                    stock = await cols[3].inner_text()
                    
                    products.append({
                        "platform": "mo店+",
                        "name": name.strip(),
                        "price": price.replace(',', '').replace('$', '').replace('NT', '').strip(),
                        "stock": stock.strip()
                    })
                    
            logger.info(f"mo店+: 商品資料擷取完成，共 {len(products)} 筆")
            return products
        except Exception as e:
            logger.error(f"mo店+ 商品同步發生問題: {e}")
            return []
        finally:
            await self.cleanup(p, browser)
        
    async def fetch_orders(self):
        """抓取 mo店+ 最新訂單"""
        p, browser, context, page = await self._init_browser()
        try:
            logger.info("mo店+: 導覽至登入頁面...")
            await page.goto("https://3p.momo.com.tw/") 
            
            # 給予使用者 60 秒的充裕時間進行手動登入操作與圖形驗證
            logger.info("請在彈出的瀏覽器中手動完成 mo店+ 登入。等待中 (60秒)...")
            await page.wait_for_timeout(60000)
            
            logger.info("mo店+: 正在尋找並切入包含訂單資料的 iframe...")
            # 遍歷所有 frames 尋找帶有 mot-table 的 iframe
            target_frame = None
            
            # 給予 iframe 載入時間
            await asyncio.sleep(5)
            
            for f in page.frames:
                try:
                    # 快速檢查該 frame 內是否有目標 table，不等待避免卡死
                    if await f.query_selector('table.mot-table'):
                        target_frame = f
                        break
                except Exception:
                    pass
                    
            if not target_frame:
                raise Exception("無法在任何 iframe 中找到訂單表格 (table.mot-table)")
            
            logger.info(f"mo店+: ✅ 成功鎖定目標 iframe (URL: {target_frame.url})")
            
            logger.info("mo店+: 正在擷取框架內的宅配訂單資料...")
            orders = []
            
            rows = await target_frame.query_selector_all('table.mot-table tbody tr')
            for row in rows:
                cols = await row.query_selector_all('td')
                if len(cols) >= 23:
                    # 輔助函式：如果有下拉選單則抓取選取值，否則取文字
                    async def get_text_or_select(td_element) -> str:
                        js_code = """
                        (td) => {
                            let select = td.querySelector('select');
                            if (select) {
                                if (select.selectedIndex >= 0) {
                                    return select.options[select.selectedIndex].text.trim();
                                }
                                return "";
                            }
                            let input = td.querySelector('input');
                            if (input && input.value) {
                                return input.value.trim();
                            }
                            return td.innerText.trim();
                        }
                        """
                        try:
                            res = await td_element.evaluate(js_code)
                            return str(res) if res else ""
                        except Exception:
                            return ""
                        
                    order_id = await get_text_or_select(cols[1])
                    status = await get_text_or_select(cols[2])
                    delivery_date = await get_text_or_select(cols[3])
                    logistics_co = await get_text_or_select(cols[4])
                    pack_type1 = await get_text_or_select(cols[5])
                    pack_type2 = await get_text_or_select(cols[6])
                    pack_weight = await get_text_or_select(cols[7])
                    order_category = await get_text_or_select(cols[8])
                    cust_requirement = await get_text_or_select(cols[9])
                    invoice_tax_id = await get_text_or_select(cols[10])
                    four_machines = await get_text_or_select(cols[11])
                    transfer_date = await get_text_or_select(cols[12])
                    latest_ship_date = await get_text_or_select(cols[13])
                    
                    # 拆解 收件人姓名 電話 地址 (換行分隔)
                    recipient_info_raw = await get_text_or_select(cols[14])
                    recipient_parts = [p.strip() for p in recipient_info_raw.split('\n') if p.strip()]
                    recip_name = recipient_parts[0] if len(recipient_parts) > 0 else ""
                    recip_phone = recipient_parts[1] if len(recipient_parts) > 1 else ""
                    recip_addr = " ".join(recipient_parts[2:]) if len(recipient_parts) > 2 else ""
                    
                    product_origin_id = await get_text_or_select(cols[15])
                    
                    # 拆解 商品編號 商品名稱 單品規格
                    product_info_raw = await get_text_or_select(cols[16])
                    product_parts = [p.strip() for p in product_info_raw.split('．') if p.strip()]
                    prod_id = product_parts[0] if len(product_parts) > 0 else ""
                    prod_name = product_parts[1] if len(product_parts) > 1 else product_info_raw
                    prod_spec = product_parts[2] if len(product_parts) > 2 else ""
                    
                    prod_qty = await get_text_or_select(cols[17])
                    amount_raw = await get_text_or_select(cols[18])
                    amount = amount_raw.replace(',', '').replace('$', '').strip() if amount_raw else "0"
                    
                    prod_attr = await get_text_or_select(cols[19])
                    tax_type = await get_text_or_select(cols[20])
                    invoice_amount = await get_text_or_select(cols[21])
                    purchaser_name = await get_text_or_select(cols[22])
                    
                    # 統一整理入 platform_details (共提供 28 個欄位資訊對應)
                    platform_details = {
                        "配送訊息": status,
                        "指定配送日": delivery_date,
                        "物流公司": logistics_co,
                        "出貨包材": pack_type1,
                        "包材類型": pack_type2,
                        "包材重量": pack_weight,
                        "訂單類別": order_category,
                        "客戶配送需求": cust_requirement,
                        "發票開立統編": invoice_tax_id,
                        "廢四機回收": four_machines,
                        "轉單日": transfer_date,
                        "最晚出貨日": latest_ship_date,
                        "收件人姓名": recip_name,
                        "電話": recip_phone,
                        "地址": recip_addr,
                        "商品原廠編號": product_origin_id,
                        "商品編號": prod_id,
                        "商品名稱": prod_name,
                        "單品規格": prod_spec,
                        "商品屬性": prod_attr,
                        "應稅免稅": tax_type,
                        "發票開立金額": invoice_amount,
                        "訂購人姓名": purchaser_name
                    }
                    
                    status_clean = status.replace('\n', ' ').strip()
                    
                    orders.append({
                        "platform": "mo店+ (宅配)",
                        "order_id": order_id,
                        "status": status_clean,
                        "amount": amount,
                        "customer": recip_name,
                        "platform_details": platform_details
                    })
            
            logger.info(f"mo店+: 訂單資料擷取完成，共 {len(orders)} 筆")
            return orders
        except Exception as e:
            logger.error(f"mo店+ 訂單同步發生問題: {e}")
            return []
        finally:
            await self.cleanup(p, browser)
