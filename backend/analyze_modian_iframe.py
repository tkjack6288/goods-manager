from bs4 import BeautifulSoup

def analyze_iframe_html():
    try:
        with open("modian_dumps/frame_0.html", "r", encoding="utf-8") as f:
            html = f.read()
    except FileNotFoundError:
        print("FileNotFound: modian_dumps/frame_0.html")
        return
        
    soup = BeautifulSoup(html, "html.parser")
    
    # 找尋所有 table
    tables = soup.find_all("table")
    print(f"IFrame 內共找到 {len(tables)} 個 table\n")
    
    for i, table in enumerate(tables):
        class_str = table.get("class", "N/A")
        print(f"--- Table {i} (Class: {class_str}) ---")
        
        headers = [th.get_text(separator=" ", strip=True) for th in table.find_all("th")]
        if headers:
            print(f"表頭 ({len(headers)} 個欄位):")
            for idx, h in enumerate(headers):
                print(f"  [{idx}] {h}")
            
        rows = table.find_all("tr")
        if len(rows) > 0:
            print(f"資料列樣本數: {len(rows)}")
            # 印出有 td 第一筆資料，核對欄位
            for r in rows:
                cols = r.find_all("td")
                if len(cols) > 0:
                    print("  第一筆資料內容:")
                    for idx, td in enumerate(cols):
                        print(f"    [{idx}] {td.get_text(separator=' ', strip=True)}")
                    break
        print()

if __name__ == "__main__":
    analyze_iframe_html()
