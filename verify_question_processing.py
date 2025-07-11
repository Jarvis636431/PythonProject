import pandas as pd

def verify_processing():
    """
    验证question列的处理效果
    """
    original_file = '/Users/jarvis/PycharmProjects/crawler/gooood_gooood-interview_qa_clean.csv'
    processed_file = '/Users/jarvis/PycharmProjects/crawler/gooood_gooood-interview_qa_clean_question_chinese_only.csv'
    
    try:
        # 读取原始文件和处理后的文件
        print("读取文件...")
        original_df = pd.read_csv(original_file)
        processed_df = pd.read_csv(processed_file)
        
        print(f"原始文件: {len(original_df)} 行")
        print(f"处理后文件: {len(processed_df)} 行")
        
        # 显示处理前后的对比
        print("\n=== 处理前后对比 (前10个问题) ===")
        for i in range(min(10, len(original_df))):
            if pd.notna(original_df.iloc[i]['question']):
                original_q = str(original_df.iloc[i]['question'])
                processed_q = str(processed_df.iloc[i]['question'])
                
                print(f"\n第{i+1}个问题:")
                print(f"原文: {original_q[:200]}..." if len(original_q) > 200 else f"原文: {original_q}")
                print(f"处理后: {processed_q}")
                print("-" * 80)
        
        # 统计英文字符数量变化
        import re
        
        def count_english_chars(text):
            if pd.isna(text):
                return 0
            return len(re.findall(r'[a-zA-Z]', str(text)))
        
        original_english = sum(original_df['question'].apply(count_english_chars))
        processed_english = sum(processed_df['question'].apply(count_english_chars))
        
        print(f"\n=== 英文字符统计 ===")
        print(f"原始question列英文字符数: {original_english}")
        print(f"处理后question列英文字符数: {processed_english}")
        print(f"移除的英文字符数: {original_english - processed_english}")
        if original_english > 0:
            print(f"英文字符移除率: {((original_english - processed_english) / original_english * 100):.2f}%")
        
    except Exception as e:
        print(f"验证过程中出现错误: {str(e)}")

if __name__ == "__main__":
    verify_processing()