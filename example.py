from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import csv
import time

def is_chinese(text):
    return re.search(r'[\u4e00-\u9fff]', text) is not None

def extract_tags(soup):
    tag_elements = soup.select('.post-meta a')
    tags = [t.get_text(strip=True) for t in tag_elements if is_chinese(t.get_text())]
    return ' / '.join(tags)

def extract_chinese_content(soup):
    paragraphs = soup.find_all(['p', 'div'])
    chinese_texts = []
    for p in paragraphs:
        text = p.get_text(strip=True)
        chinese_sentences = re.findall(r'[\u4e00-\u9fff，。！？：；、“”‘’（）()《》]+', text)
        if chinese_sentences:
            clean_text = ''.join(chinese_sentences).strip()
            if clean_text:
                chinese_texts.append(clean_text)
    return '\n'.join(chinese_texts)

# 初始化 Selenium
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

base_list = 'https://www.gooood.cn/filter/type/all/country/all/material/all/office/all/page/{}'
base_url = 'https://www.gooood.cn'
results = []

for page in range(1, 1467):
    list_url = base_list.format(page)
    print(f'📄 列表页: {list_url}')
    driver.get(list_url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    articles = soup.select('h2.entry-title a')

    if not articles:
        print(f'⚠️ 第 {page} 页无数据，停止爬取')
        break

    for article in articles:
        relative_url = article['href']
        full_url = base_url + relative_url if not relative_url.startswith('http') else relative_url
        print(f'🔍 抓取页面: {full_url}')

        try:
            driver.get(full_url)
            time.sleep(2)

            # 检查 iframe
            try:
                iframe = driver.find_element('id', 'mainframe')
                iframe_src = iframe.get_attribute('src')
                real_url = iframe_src if iframe_src.startswith('http') else base_url + iframe_src
                driver.get(real_url)
                time.sleep(2)
                print('  ✅ 使用 iframe 页面')
            except NoSuchElementException:
                real_url = full_url
                print('  ✅ 使用原始页面')

            soup_detail = BeautifulSoup(driver.page_source, 'html.parser')

            tags = extract_tags(soup_detail)
            content = extract_chinese_content(soup_detail)

            if not content.strip():
                print(f'  ❌ 未提取到正文: {real_url}')
                continue

            results.append({
                'tags': tags,
                'content': content,
                'url': real_url
            })

        except Exception as e:
            print(f'⚠️ 抓取失败: {full_url} — {e.__class__.__name__}: {e}')
            continue

driver.quit()

# 写入 CSV
filename = 'gooood_project_content.csv'
with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=['tags', 'content', 'url'])
    writer.writeheader()
    writer.writerows(results)

print(f'\n✅ 完成采集，共 {len(results)} 条项目，保存为 {filename}')