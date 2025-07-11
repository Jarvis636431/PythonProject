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

# 检查是否包含中文
def is_chinese(text):
    return re.search(r'[\u4e00-\u9fff]', text) is not None

# 清洗回答：只保留中文句子，去掉英文和无关内容
def clean_answer_paragraph(text):
    sentences = re.split(r'[。！？]', text)
    clean_sentences = []
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        total = len(s)
        chinese = len(re.findall(r'[\u4e00-\u9fff]', s))
        if total == 0:
            continue
        if chinese / total >= 0.8:
            clean_sentences.append(s + '。')  # 保留句号
    return ''.join(clean_sentences)

# 提取问答对
def extract_qa(content_div):
    qa_pairs = []
    elements = [el for el in content_div.find_all(['p', 'div']) if isinstance(el, Tag)]
    blocklist_keywords = ['gooood', '公众号', '版权', '转载请', '投稿', '图片来自']
    i = 0
    while i < len(elements) - 1:
        question_el = elements[i]
        question_text = question_el.get_text(strip=True)

        is_q_format = question_text.startswith(('Q:', 'Q：', 'Q.', 'Q ')) or question_el.find('strong')
        if is_chinese(question_text) and is_q_format:
            j = i + 1
            while j < len(elements):
                raw_answer = elements[j].get_text(strip=True)
                if any(keyword in raw_answer for keyword in blocklist_keywords):
                    j += 1
                    continue
                clean_answer = clean_answer_paragraph(raw_answer)
                if clean_answer:
                    qa_pairs.append((question_text, clean_answer))
                    break
                j += 1
            i = j
        else:
            i += 1
    return qa_pairs

# 初始化 Selenium
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

series_name = 'gooood-interview'
base_list = f'https://www.gooood.cn/category/series/{series_name}/page/{{}}'
base_url = 'https://www.gooood.cn'
results = []

# 爬取总页数（你可以根据实际页数调整）
for page in range(1, 6):
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

            author_match = re.search(r'Interview[:：]?\s*(.+)', title)
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

# 写入 CSV 文件
filename = f'gooood_{series_name}_qa_clean.csv'
with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=['author', 'question', 'answer', 'url'])
    writer.writeheader()
    writer.writerows(results)

print(f'\n✅ 完成提取，共 {len(results)} 组问答，保存为 {filename}')