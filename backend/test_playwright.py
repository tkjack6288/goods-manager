import asyncio
from playwright.async_api import async_playwright

async def test_playwright():
    print("Starting Playwright test...")
    async with async_playwright() as p:
        print("Launching Chromium (headless=False)...")
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        print("Navigating to example.com...")
        await page.goto("https://example.com")
        
        print("Waiting 3 seconds...")
        await asyncio.sleep(3)
        
        title = await page.title()
        print(f"Page title: {title}")
        
        print("Closing browser...")
        await browser.close()
    print("Test finished successfully.")

if __name__ == "__main__":
    if hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
        # Windows 上使用 playwright 需要設定 EventLoopPolicy，尤其是跟其他 async 框架混用時
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(test_playwright())
