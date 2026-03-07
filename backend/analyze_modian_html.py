from bs4 import BeautifulSoup
import json

def analyze_html():
    try:
        with open("modian_orders_dump.html", "r", encoding="utf-8") as f:
            html = f.read()
    except FileNotFoundError:
        print("未找到 modian_orders_dump.html 檔案")
        return
        
    soup = BeautifulSoup(html, "html.parser")
    
    # 尋找所有可能的表格
    tables = soup.find_all("table")
    print(f"找到 {len(tables)} 個 <table> 元素\n")
    
    for i, table in enumerate(tables):
        print(f"--- 表格 {i+1} ---")
        print(f"Class: {table.get('class')}")
        
        # 找表頭
        headers = [th.get_text(strip=True) for th in table.find_all("th")]
        if headers:
            print(f"表頭: {headers}")
            
        # 找前兩筆資料
        rows = table.find_all("tr")
        if len(rows) > 1:
            print("資料樣本:")
            data_rows = rows[1:3] if headers else rows[0:2]
            for r in data_rows:
                cols = [td.get_text(strip=True) for td in r.find_all("td")]
                if cols:
                    print(f"  {cols}")
        print("\n")
        
    # 如果沒找到傳統 table，找 div based list (常見於現代框架)
    print("--- 尋找疑似訂單列的 Div (包含 '單號', '狀態' 等關鍵字) ---")
    potential_rows = soup.find_all(lambda tag: tag.name == "div" and tag.get("class") and any("row" in c.lower() or "item" in c.lower() or "list" in c.lower() for c in tag.get("class", [])))
    
    found_div_rows = 0
    for div in potential_rows:
        text = div.get_text(separator=" | ", strip=True)
        # 簡單過濾一下，假設訂單列會有一堆資訊
        if len(text) > 30 and ("訂單" in text or "狀態" in text or "NT$" in text or "$" in text):
            print(f"Div Class {div.get('class')}: {text[:100]}...")
            found_div_rows += 1
            if found_div_rows >= 3:
                break
                
    if found_div_rows == 0:
        # 單純用文字搜尋印出附近結構
        import re
        for text_node in soup.find_all(text=re.compile(r"訂單|訂單編號|單號")):
            parent = text_node.parent
            grandparent = parent.parent if parent else None
            
            print(f"找到關鍵字 '{text_node.strip()}'，位於: <{parent.name} class='{parent.get('class')}'> 內")
            if grandparent:
                 print(f"  祖父節點: <{grandparent.name} class='{grandparent.get('class')}>'")
            break # 印一個就好

if __name__ == "__main__":
    analyze_html()
