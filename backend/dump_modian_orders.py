import asyncio
from playwright.async_api import async_playwright
import sys
import os

async def dump_html():
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
    print("啟動 Playwright...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        url = "https://3p.momo.com.tw/"
        print(f"導覽至 mo店+ 入口 {url}，請手動進行登入。")
        await page.goto(url)
        
        print("\n=======================================================")
        print("請在彈出的瀏覽器中完成以下步驟：")
        print("1. 登入 mo店+ 後台")
        print("2. 點擊進入「訂單管理 / 出貨處理」等能看到訂單列表的頁面")
        print("3. 等待訂單列表完全載入")
        print("完成上述步驟後，請在這個終端機視窗按下 [Enter] 鍵繼續...")
        print("=======================================================\n")
        
        await asyncio.to_thread(input)
        
        print("正在擷取主頁面與所有 iframe 的 HTML 結構...")
        
        # 建立儲存資料夾
        os.makedirs("modian_dumps", exist_ok=True)
        
        # 1. 主頁面
        main_html = await page.content()
        with open("modian_dumps/main.html", "w", encoding="utf-8") as f:
            f.write(main_html)
            
        # 2. 所有 IFrame
        for i, frame in enumerate(page.frames):
            try:
                frame_html = await frame.content()
                # 只儲存內容有一定長度的 frame，過濾掉廣告或空白 frame
                if len(frame_html) > 1000:
                    with open(f"modian_dumps/frame_{i}.html", "w", encoding="utf-8") as f:
                        f.write(frame_html)
                    print(f"✅ 成功儲存 Frame {i} (URL: {frame.url})")
            except Exception as e:
                print(f"無法讀取 Frame {i}: {e}")
                
        print("\n所有 HTML 已成功儲存至 modian_dumps/ 資料夾下！")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(dump_html())
