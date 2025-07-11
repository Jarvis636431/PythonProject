import pandas as pd
import re

def remove_english_text(text):
    if pd.isna(text) or text == '':
        return text
    
    # 转换为字符串
    text = str(text)
    
    # 1. 移除倒三角号及其后面的所有内容
    text = re.sub(r'▼.*$', '', text, flags=re.MULTILINE)
    
    # 2. 移除英文字母、数字和英文标点符号的组合
    # 保留中文字符、中文标点符号、空格
    text = re.sub(r'[a-zA-Z0-9]+[\s]*[a-zA-Z0-9]*', '', text)
    
    # 3. 移除常见的英文标点符号和特殊字符
    text = re.sub(r'[\[\]{}()"\'\/\\|<>@#$%^&*+=~`]', '', text)
    
    # 4. 移除URL相关内容
    text = re.sub(r'http[s]?://[^\s]*', '', text)
    text = re.sub(r'www\.[^\s]*', '', text)
    text = re.sub(r'://[^\s]*', '', text)
    
    # 5. 移除多余的标点符号
    # 移除连续的逗号
    text = re.sub(r',{2,}', ',', text)
    # 移除连续的句号
    text = re.sub(r'\.{2,}', '。', text)
    # 移除连续的问号
    text = re.sub(r'\?{2,}', '？', text)
    # 移除连续的感叹号
    text = re.sub(r'!{2,}', '！', text)
    
    # 6. 移除行首行尾的标点符号
    text = re.sub(r'^[,，.。?？!！;；:：\s]+', '', text)
    text = re.sub(r'[,，.。?？!！;；:：\s]+$', '', text)
    
    # 7. 移除多余的空格
    text = re.sub(r'\s+', ' ', text)
    
    # 8. 移除只包含标点符号的内容
    if re.match(r'^[,，.。?？!！;；:：\s]*$', text):
        return ''
    
    return text.strip()

def clean_csv_file(input_file, output_file):
    print(f"正在处理文件: {input_file}")
    
    # 读取CSV文件
    df = pd.read_csv(input_file, encoding='utf-8')
    print(f"原始数据: {df.shape[0]} 行, {df.shape[1]} 列")
    
    # 处理每一列，但跳过url列
    for col in df.columns:
        if col.lower() == 'url':  # 跳过url列，保留原始URL内容
            print(f"跳过URL列: {col}")
            continue
        print(f"正在处理列: {col}")
        df[col] = df[col].apply(remove_english_text)
    
    # 移除完全为空的行
    df = df.dropna(how='all')
    
    # 移除所有列都为空字符串的行
    df = df[~(df == '').all(axis=1)]
    
    print(f"处理后数据: {df.shape[0]} 行, {df.shape[1]} 列")
    
    # 保存处理后的文件
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"文件已保存到: {output_file}")

def main():
    input_file = '/Users/jarvis/PycharmProjects/crawler/gooood_gooood-interview_qa_clean.csv'
    output_file = '/Users/jarvis/PycharmProjects/crawler/gooood_gooood-interview_qa_clean_chinese_only.csv'
    
    clean_csv_file(input_file, output_file)
    print("处理完成！")

if __name__ == "__main__":
    main()