import pandas as pd
import re

def remove_english_from_question(text):
    """
    从question文本中移除英文内容，只保留中文部分
    """
    if pd.isna(text) or text == '':
        return text
    
    # 移除英文字母、数字和常见英文标点符号
    # 保留中文字符、中文标点符号
    text = re.sub(r'[a-zA-Z0-9]+', '', text)
    text = re.sub(r'[.,;:!?"\'\'\"\(\)\[\]\{\}\-_+=<>/\\|`~@#$%^&*]', '', text)
    
    # 清理多余的空格和标点符号
    text = re.sub(r'\s+', '', text)  # 移除所有空格
    text = re.sub(r'[。，；：！？、]+', '？', text)  # 统一中文标点
    
    # 移除开头和结尾的标点符号
    text = text.strip('？。，；：！、')
    
    return text

def process_csv_file():
    """
    处理CSV文件，移除question列中的英文内容
    """
    input_file = '/Users/jarvis/PycharmProjects/crawler/gooood_gooood-interview_qa_clean.csv'
    output_file = '/Users/jarvis/PycharmProjects/crawler/gooood_gooood-interview_qa_clean_question_chinese_only.csv'
    
    try:
        # 读取CSV文件
        print(f"正在读取文件: {input_file}")
        df = pd.read_csv(input_file)
        print(f"文件读取成功，共 {len(df)} 行，{len(df.columns)} 列")
        print(f"列名: {list(df.columns)}")
        
        # 检查是否存在question列
        if 'question' not in df.columns:
            print("错误：文件中没有找到'question'列")
            return
        
        # 处理question列
        print("正在处理question列...")
        df['question'] = df['question'].apply(remove_english_from_question)
        
        # 保存处理后的文件
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"处理完成，结果已保存到: {output_file}")
        
        # 显示处理前后的对比示例
        print("\n处理效果预览（前5行question列）:")
        original_df = pd.read_csv(input_file)
        for i in range(min(5, len(df))):
            if pd.notna(original_df.iloc[i]['question']) and pd.notna(df.iloc[i]['question']):
                print(f"原文: {original_df.iloc[i]['question'][:100]}...")
                print(f"处理后: {df.iloc[i]['question']}")
                print("-" * 50)
        
    except Exception as e:
        print(f"处理过程中出现错误: {str(e)}")

if __name__ == "__main__":
    process_csv_file()