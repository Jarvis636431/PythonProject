from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import csv
import time
from bs4.element import Tag

def is_chinese(text):
    return re.search(r'[\u4e00-\u9fff]', text) is not None

def extract_qa(content_div):
    qa_pairs = []
    elements = [el for el in content_div.find_all(['p', 'div']) if isinstance(el, Tag)]
    i = 0
    while i < len(elements) - 1:
        question_el = elements[i]
        answer_el = elements[i + 1]

        if question_el.find('strong'):
            question_text = question_el.get_text(strip=True)
            if is_chinese(question_text) and len(question_text) < 100:
                answer_text = answer_el.get_text(strip=True)
                if is_chinese(answer_text) and not answer_el.find('strong'):
                    qa_pairs.append((question_text, answer_text))
                    i += 2
                    continue
        i += 1
    return qa_pairs

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

series_name = 'oversea'
base_list = f'https://www.gooood.cn/category/series/{series_name}/page/{{}}'
base_url = 'https://www.gooood.cn'
results = []

for page in range(1, 9):
    list_url = base_list.format(page)
    print(f'📄 抓取列表页: {list_url}')
    driver.get(list_url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    articles = soup.select('h2.entry-title a')

    for article in articles:
        title = article.text.strip()
        relative_url = article['href']
        full_url = base_url + relative_url if not relative_url.startswith('http') else relative_url
        print(f'🔍 抓取文章: {title}')

        try:
            driver.get(full_url)
            time.sleep(2)
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
            content_div = soup_detail.find('body')
            if not content_div:
                print(f'  ❌ 无正文内容: {real_url}')
                continue

            author_match = re.search(r'Overseas\\s+NO\\.\\d+[:：]?\\s*(.+)', title)
            author = author_match.group(1).strip() if author_match else ""

            qa_list = extract_qa(content_div)
            for q, a in qa_list:
                results.append({
                    'author': author,
                    'question': q,
                    'answer': a,
                    'url': real_url
                })

        except Exception as e:
            print(f'⚠️ 错误: {full_url} — {e.__class__.__name__}: {e}')
            continue

driver.quit()

filename = f'gooood_{series_name}_qa_clean.csv'
with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=['author', 'question', 'answer', 'url'])
    writer.writeheader()
    writer.writerows(results)

print(f'\n✅ 提取完成，共 {len(results)} 组问答，保存为 {filename}')