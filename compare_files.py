#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对比处理前后的CSV文件统计信息
"""

import pandas as pd
import re

def count_english_chars(text):
    """统计文本中的英文字符数量"""
    if pd.isna(text):
        return 0
    return len(re.findall(r'[a-zA-Z]', str(text)))

def count_chinese_chars(text):
    """统计文本中的中文字符数量"""
    if pd.isna(text):
        return 0
    return len(re.findall(r'[\u4e00-\u9fff]', str(text)))

def analyze_file(file_path, file_name):
    """分析单个文件"""
    print(f"\n=== {file_name} ===")
    
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        print(f"总行数: {len(df)}")
        print(f"总列数: {len(df.columns)}")
        
        # 统计主要列的字符数
        main_columns = ['author', 'question', 'answer', 'url']
        existing_columns = [col for col in main_columns if col in df.columns]
        
        total_english = 0
        total_chinese = 0
        
        for col in existing_columns:
            english_count = df[col].apply(count_english_chars).sum()
            chinese_count = df[col].apply(count_chinese_chars).sum()
            total_english += english_count
            total_chinese += chinese_count
            print(f"{col}列 - 英文字符: {english_count}, 中文字符: {chinese_count}")
        
        print(f"\n总计:")
        print(f"英文字符总数: {total_english}")
        print(f"中文字符总数: {total_chinese}")
        print(f"英文占比: {total_english/(total_english+total_chinese)*100:.2f}%")
        print(f"中文占比: {total_chinese/(total_english+total_chinese)*100:.2f}%")
        
        return total_english, total_chinese
        
    except Exception as e:
        print(f"分析文件时出错: {str(e)}")
        return 0, 0

def main():
    original_file = '/Users/jarvis/PycharmProjects/crawler/gooood_gooood-interview_qa_clean.csv'
    processed_file = '/Users/jarvis/PycharmProjects/crawler/gooood_gooood-interview_qa_clean_chinese_only.csv'
    
    print("CSV文件处理前后对比分析")
    print("=" * 50)
    
    # 分析原始文件
    orig_eng, orig_chi = analyze_file(original_file, "原始文件")
    
    # 分析处理后文件
    proc_eng, proc_chi = analyze_file(processed_file, "处理后文件")
    
    # 对比结果
    print(f"\n=== 处理效果对比 ===")
    print(f"英文字符减少: {orig_eng - proc_eng} ({(orig_eng - proc_eng)/orig_eng*100:.2f}%)")
    print(f"中文字符保留: {proc_chi} ({proc_chi/orig_chi*100:.2f}%)")
    
    if proc_eng == 0:
        print("\n✅ 成功！所有英文内容已被完全移除")
    else:
        print(f"\n⚠️  仍有 {proc_eng} 个英文字符未被移除")

if __name__ == '__main__':
    main()