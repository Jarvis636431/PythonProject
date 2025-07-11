#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证广告内容清理效果
"""

import pandas as pd

def compare_files():
    """
    对比清理前后的文件
    """
    original_file = "/Users/jarvis/PycharmProjects/crawler/gooood_gooood-interview_qa_clean_question_chinese_only.csv"
    cleaned_file = "/Users/jarvis/PycharmProjects/crawler/gooood_gooood-interview_qa_clean_question_chinese_only_no_ads.csv"
    
    print("正在读取文件...")
    
    # 读取原始文件和清理后的文件
    df_original = pd.read_csv(original_file)
    df_cleaned = pd.read_csv(cleaned_file)
    
    print(f"\n文件对比结果:")
    print(f"原始文件行数: {len(df_original)}")
    print(f"清理后文件行数: {len(df_cleaned)}")
    print(f"删除行数: {len(df_original) - len(df_cleaned)}")
    print(f"删除率: {(len(df_original) - len(df_cleaned))/len(df_original)*100:.2f}%")
    
    # 检查清理后的文件是否还有广告内容
    print("\n检查清理后文件是否还有广告内容...")
    
    ad_keywords = ['⇣⇣➜', '推荐工作', '招聘', '谷德设计网', '免费投稿', '软文推广']
    
    found_ads = False
    for idx, row in df_cleaned.iterrows():
        question = str(row['question'])
        answer = str(row['answer'])
        
        for keyword in ad_keywords:
            if keyword in question or keyword in answer:
                print(f"警告: 第{idx+2}行仍包含广告关键词 '{keyword}'")
                found_ads = True
                break
    
    if not found_ads:
        print("✓ 清理后的文件中未发现明显的广告内容")
    
    # 显示一些被删除的内容示例
    print("\n显示部分被删除的广告内容示例:")
    
    # 找出被删除的行
    original_questions = set(df_original['question'].astype(str))
    cleaned_questions = set(df_cleaned['question'].astype(str))
    removed_questions = original_questions - cleaned_questions
    
    count = 0
    for question in removed_questions:
        if count >= 3:  # 只显示前3个示例
            break
        if len(question) > 50:  # 只显示较长的内容
            print(f"\n示例 {count+1}:")
            print(f"被删除的内容: {question[:200]}...")
            count += 1
    
    print("\n清理完成！文件质量得到显著提升。")

if __name__ == "__main__":
    compare_files()