#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理CSV文件中的广告和推广内容
"""

import pandas as pd
import re

def is_advertisement_content(text):
    """
    判断文本是否为广告内容
    """
    if not isinstance(text, str) or not text.strip():
        return False
    
    # 广告内容的特征关键词
    ad_keywords = [
        '⇣⇣➜关于我们➜', '免费投稿', '招聘人才', '人才求职', '软文推广', '图文推广',
        '找设计师找业主', '其他问询推广', '深耕建筑交互留学', '施工图深化设计',
        '建筑留学值得信赖', '行之建筑平凡中造非凡', '推荐工作提交新工作',
        '所有工作»', '最新工作提交新工作', '设计总监主创建筑师', '建筑师助理建筑师实习生',
        '高级建筑设计师', '项目建筑师', '中级建筑设计师', '中级室内设计师',
        '初级建筑设计师', '设计实习生', '项目设计师助理设计师', '商务行政专员',
        '媒体助理', '主创建筑师项目建筑师', '室内设计师高级技术总监', '商务经理',
        '全职编辑', '公关外联编辑', '方案建筑师建筑实习生', '软装设计师驻场设计师',
        '媒体运营专员实习生', '最近有哪些好工作', '谷德最新家招聘信息汇总',
        '品牌负责人展陈室内设计师', '公共艺术与装置设计师', '研究员学术助理',
        '内容策划商务运营经理', '长期招聘', '资深室内主案设计师', '资深建筑主案设计师',
        '资深物料软装设计师', '效果图设计师设计助理', '城市设计师方案精细化',
        '项目主任方案精细化设计师', '品牌及学术方向岗位', '研究与媒体专员',
        '长期有效', '项目负责人高级建筑师', '实习建筑师', '硬装设计总监',
        '软装设计总监主案设计师', '硬装软装', '总监资深室内设计师',
        '平面视觉设计师项目经理', '中后期负责人媒体公关负责人', '服务体验设计师',
        '收藏本文分享到', '发表评论您需要登录以发表评论', '社交登录评论用户名',
        '回复这些东西为什么能落地的', '染净识回复', '奇怪的美感回复',
        '我是做室内设计的', '通过此文章', '觉得的设计很丑很丑',
        '至少这个文章中项目是这样的', '回复回复能说出这种话',
        '你自己的室内作品美感也不会好到哪去', '或者根本没有美感可谈',
        '永远有多远回复', '讲真每次路过三环', '感觉大裤衩还是很不错的',
        '所以好的建筑是不是都具有超前属性', '感觉像个实际干活的',
        '和老酷头气质类型不一样回复', '的理论及方案一直都挺有趣的',
        '想法也蛮新颖', '角度多元独特的新颖', '隐约自带批判属性',
        '高产的同时也考虑到了很多人文关怀', '方案设计的过程给作为学生的自己有很大的启发性',
        '鼓励用不同的角度去思考建筑的存在本身', '不过诚实的说作为使用者目前还没有过任何有触动自己的建筑空间体验',
        '去过', '可能理论放至实践的过程太短', '呈现的结果对于使用者都有点像是个怪兽',
        '可能是这一种设计建筑的方式和做成就是极其困难吧', '很多重要的项目都是远脱出人尺度的巨型',
        '谷德设计网首页专辑', '所有专辑访谈专辑', '办公室真相未满岁创意人记录',
        '大周年每个人在海外日常深度', '未建成材料与细部想法专辑',
        '信步辑先锋专辑其他专辑', '分类建筑景观设计艺术资讯合集',
        '复合检索关于谷德投稿与推广', '投稿谷德文章推广图文广告',
        '工作招聘我是求职者', '查看所有好工作我是雇主', '如何发布好工作项目对接',
        '我是业主方', '寻优秀设计师我是设计方', '如何承接项目正在寻找设计师的全部项目',
        '项目对接成功案例精选', '搜索收藏加入默认收藏夹', '新建收藏夹复合收藏为会员专享功能',
        '开通会员即可体验分享会员登录', '访谈专辑第三十一期', '用激进的设计解决许多国家面临的城市问题',
        '第届厦门国际石材展', '项目标签设计公司位置荷兰类型专辑建筑访谈专辑标签',
        '团队采访世界各地的有趣创意人', '欢迎您的推荐和建议', '第期为您奉上的是创始人的访谈',
        '更多关于他', '请至', '出品人', '向玲编辑团队', '陈诺嘉', '武晨曦', '李诗蓉', '徐馨羽', '李禹潺'
    ]
    
    # 检查是否包含广告关键词
    for keyword in ad_keywords:
        if keyword in text:
            return True
    
    # 检查是否为纯粹的导航或推广文本（长度超过200且包含大量特殊符号）
    if len(text) > 200:
        special_chars_count = sum(1 for char in text if char in '⇣⇡➜◎–»（）')
        if special_chars_count > 10:
            return True
    
    # 检查是否为评论区内容
    comment_patterns = [
        r'回复.*?回复',
        r'用户名回复',
        r'社交登录评论',
        r'发表评论您需要登录',
        r'收藏本文分享到'
    ]
    
    for pattern in comment_patterns:
        if re.search(pattern, text):
            return True
    
    return False

def clean_csv_content(input_file, output_file):
    """
    清理CSV文件中的广告内容
    """
    print(f"正在读取文件: {input_file}")
    
    # 读取CSV文件
    df = pd.read_csv(input_file)
    
    print(f"原始文件包含 {len(df)} 行数据")
    
    # 统计清理前的数据
    original_rows = len(df)
    
    # 清理question列中的广告内容
    if 'question' in df.columns:
        # 标记需要删除的行
        rows_to_remove = []
        
        for idx, row in df.iterrows():
            question = row['question']
            if is_advertisement_content(question):
                rows_to_remove.append(idx)
                print(f"发现广告内容 (行 {idx+2}): {str(question)[:100]}...")
        
        # 删除包含广告内容的行
        if rows_to_remove:
            df = df.drop(rows_to_remove)
            df = df.reset_index(drop=True)
            print(f"删除了 {len(rows_to_remove)} 行广告内容")
        else:
            print("未发现需要删除的广告内容")
    
    # 清理answer列中可能的广告内容
    if 'answer' in df.columns:
        answer_rows_to_remove = []
        
        for idx, row in df.iterrows():
            answer = row['answer']
            if is_advertisement_content(answer):
                answer_rows_to_remove.append(idx)
                print(f"发现answer中的广告内容 (行 {idx+2}): {str(answer)[:100]}...")
        
        if answer_rows_to_remove:
            df = df.drop(answer_rows_to_remove)
            df = df.reset_index(drop=True)
            print(f"删除了 {len(answer_rows_to_remove)} 行包含广告内容的answer")
    
    # 保存清理后的文件
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    cleaned_rows = len(df)
    removed_rows = original_rows - cleaned_rows
    
    print(f"\n清理完成！")
    print(f"原始行数: {original_rows}")
    print(f"清理后行数: {cleaned_rows}")
    print(f"删除行数: {removed_rows}")
    print(f"删除率: {removed_rows/original_rows*100:.2f}%")
    print(f"清理后的文件已保存到: {output_file}")
    
    return df

if __name__ == "__main__":
    input_file = "/Users/jarvis/PycharmProjects/crawler/gooood_gooood-interview_qa_clean_question_chinese_only.csv"
    output_file = "/Users/jarvis/PycharmProjects/crawler/gooood_gooood-interview_qa_clean_question_chinese_only_no_ads.csv"
    
    clean_csv_content(input_file, output_file)