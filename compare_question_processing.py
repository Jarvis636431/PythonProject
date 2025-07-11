#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

def compare_files():
    """
    对比处理前后的question列内容
    """
    # 读取原始文件和处理后的文件
    original_df = pd.read_csv("/Users/jarvis/PycharmProjects/crawler/gooood_oversea_qa_clean.csv")
    processed_df = pd.read_csv("/Users/jarvis/PycharmProjects/crawler/gooood_oversea_qa_clean_chinese_only.csv")
    
    print("=== Question列处理前后对比 ===")
    print(f"原始文件行数: {len(original_df)}")
    print(f"处理后文件行数: {len(processed_df)}")
    print()
    
    # 显示前10个问题的对比
    print("前10个问题的处理对比:")
    print("-" * 80)
    
    for i in range(min(10, len(original_df))):
        original_q = original_df.iloc[i]['question'] if pd.notna(original_df.iloc[i]['question']) else "(空)"
        processed_q = processed_df.iloc[i]['question'] if pd.notna(processed_df.iloc[i]['question']) else "(空)"
        
        print(f"第{i+1}行:")
        print(f"  原始: {original_q}")
        print(f"  处理后: {processed_q}")
        print()
    
    # 统计英文字符数量变化
    def count_english_chars(text):
        if pd.isna(text):
            return 0
        import re
        english_chars = re.findall(r'[a-zA-Z]', str(text))
        return len(english_chars)
    
    original_english_count = original_df['question'].apply(count_english_chars).sum()
    processed_english_count = processed_df['question'].apply(count_english_chars).sum()
    
    print("=== 英文字符统计 ===")
    print(f"原始question列英文字符数: {original_english_count}")
    print(f"处理后question列英文字符数: {processed_english_count}")
    print(f"移除的英文字符数: {original_english_count - processed_english_count}")
    print(f"英文字符移除率: {((original_english_count - processed_english_count) / original_english_count * 100):.2f}%")

if __name__ == "__main__":
    compare_files()