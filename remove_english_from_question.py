#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import re

def remove_english_from_question(text):
    """
    从问题文本中移除英文部分，保留中文部分
    """
    if pd.isna(text) or text == '':
        return text
    
    # 移除英文字母、数字、常见英文标点符号
    # 保留中文字符、中文标点符号
    cleaned_text = re.sub(r'[a-zA-Z0-9\s\?\!\.,;:()\[\]{}"\'\/\-_=+*&%$#@~`|\\]+', '', text)
    
    # 清理多余的标点符号和空格
    cleaned_text = re.sub(r'[？]+', '？', cleaned_text)  # 多个问号合并为一个
    cleaned_text = re.sub(r'[。]+', '。', cleaned_text)  # 多个句号合并为一个
    cleaned_text = re.sub(r'[，]+', '，', cleaned_text)  # 多个逗号合并为一个
    cleaned_text = re.sub(r'^[，。？！；：]+', '', cleaned_text)  # 移除开头的标点符号
    cleaned_text = re.sub(r'[，。？！；：]+$', '', cleaned_text)  # 移除结尾多余的标点符号，但保留问号
    
    # 如果原文以问号结尾，确保清理后的文本也以问号结尾
    if text.strip().endswith('?') or text.strip().endswith('？'):
        if not cleaned_text.endswith('？'):
            cleaned_text += '？'
    
    return cleaned_text.strip()

def process_csv_file(input_file, output_file):
    """
    处理CSV文件，移除question列中的英文内容
    """
    print(f"正在读取文件: {input_file}")
    
    # 读取CSV文件
    df = pd.read_csv(input_file)
    
    print(f"原始数据: {len(df)} 行, {len(df.columns)} 列")
    
    # 处理question列
    if 'question' in df.columns:
        print("正在处理question列...")
        df['question'] = df['question'].apply(remove_english_from_question)
        print("question列处理完成")
    else:
        print("警告: 未找到question列")
    
    # 保存处理后的文件
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"处理完成，已保存到: {output_file}")
    
    # 显示前几行预览
    print("\n处理后的前5行预览:")
    print(df[['question', 'answer']].head())
    
    return df

if __name__ == "__main__":
    input_file = "/Users/jarvis/PycharmProjects/crawler/gooood_oversea_qa_clean.csv"
    output_file = "/Users/jarvis/PycharmProjects/crawler/gooood_oversea_qa_clean_chinese_only.csv"
    
    process_csv_file(input_file, output_file)