import re
with open(r'C:\Users\Administrator\Documents\New project\jd_debug3.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Find all script src
scripts = re.findall(r'<script[^>]*src="([^"]+)"', text)
print('Script sources:')
for s in scripts[:20]:
    print(f'  {s[:150]}')

# Look for search/list API endpoints
apis = re.findall(r'https?://[^\s"\'<>]*(?:search|list|ware|product)[^\s"\'<>]*', text)
print(f'\nSearch/list API URLs ({len(apis)}):')
for a in apis[:10]:
    print(f'  {a}')

# Check for data-* attributes with product info
print(f'\nContains "ware": {"ware" in text.lower()}')
print(f'Contains "price": {"price" in text.lower()}')
print(f'Contains "product": {"product" in text.lower()}')
print(f'Length: {len(text)}')

# Check if there are any <li> items
li_count = len(re.findall(r'<li[^>]*>', text))
print(f'LI tags: {li_count}')

# Check for script containing JSON
json_scripts = re.findall(r'<script[^>]*type=["\']application/json["\'][^>]*>(.*?)</script>', text, re.DOTALL)
print(f'JSON script blocks: {len(json_scripts)}')
if json_scripts:
    print(f'First JSON: {json_scripts[0][:300]}')

# Check the last part of the page
print(f'\nLast 500 chars:\n{text[-500:]}')
