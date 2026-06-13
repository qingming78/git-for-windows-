import requests
from bs4 import BeautifulSoup
import re, json, os

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://www.jd.com/',
}

def fetch_page(keyword, page=1):
    url = f'https://search.jd.com/Search?keyword={keyword}&page={page}&enc=utf-8'
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.encoding = 'utf-8'
        return r.text
    except Exception as e:
        print(f"请求失败: {e}")
        return None

def parse_items(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = []
    for gl in soup.select('.gl-item'):
        try:
            # 商品名称
            name_el = gl.select_one('.p-name a em')
            if not name_el:
                continue
            name = name_el.get_text(strip=True)

            # 价格
            price_el = gl.select_one('.p-price strong')
            if not price_el:
                continue
            price_text = price_el.get_text(strip=True).replace(',', '')
            price = float(re.sub(r'[^\d.]', '', price_text))

            # 店铺名称
            shop_el = gl.select_one('.p-shop a') or gl.select_one('.J_im_icon a') or gl.select_one('.curr-shop')
            shop = shop_el.get_text(strip=True) if shop_el else '未知店铺'
            shop = re.sub(r'\s+', '', shop)

            items.append({'name': name, 'price': price, 'shop': shop})
        except:
            continue
    return items

def main():
    keyword = '联想拯救者y9000p'
    all_items = []
    seen = set()

    for page in [1, 2]:
        print(f"正在抓取第 {page} 页...")
        html = fetch_page(keyword, page)
        if not html:
            continue
        items = parse_items(html)
        for item in items:
            key = (item['name'][:20], item['price'])
            if key not in seen:
                seen.add(key)
                all_items.append(item)
        print(f"  第 {page} 页: {len(items)} 条")

    # 按价格排序
    all_items.sort(key=lambda x: x['price'])

    # 输出到文件
    output_dir = r'C:\Users\Administrator\Documents\New project'
    json_path = os.path.join(output_dir, 'jd_results.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)
    print(f"\n共找到 {len(all_items)} 件商品，已保存到 {json_path}")
    print(f"\n{'价格':>10}  {'商家':<20}  {'商品名称'}")
    print('-' * 120)
    for item in all_items:
        print(f"¥{item['price']:>7.2f}  {item['shop']:<20}  {item['name'][:50]}")

if __name__ == '__main__':
    main()
