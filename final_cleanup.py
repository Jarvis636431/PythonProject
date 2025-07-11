import pandas as pd
import re

def final_cleanup_csv(input_file, output_file):
    print(f"正在进行最终清理: {input_file}")
    
    # 读取CSV文件
    df = pd.read_csv(input_file, encoding='utf-8')
    print(f"原始数据: {df.shape[0]} 行, {df.shape[1]} 列")
    
    # 1. 移除完全为空的列
    df = df.dropna(axis=1, how='all')
    
    # 2. 移除只包含空字符串的列
    df = df.loc[:, ~(df == '').all()]
    
    # 3. 移除以"Unnamed"开头的空列
    unnamed_cols = [col for col in df.columns if col.startswith('Unnamed') and df[col].isna().all()]
    df = df.drop(columns=unnamed_cols)
    
    # 4. 对剩余的文本进行最终清理
    for col in df.columns:
        if df[col].dtype == 'object':  # 文本列
            df[col] = df[col].apply(lambda x: final_text_cleanup(x) if pd.notna(x) else x)
    
    # 5. 移除完全为空的行
    df = df.dropna(how='all')
    
    # 6. 移除所有列都为空字符串的行
    mask = df.apply(lambda row: row.astype(str).str.strip().eq('').all(), axis=1)
    df = df[~mask]
    
    print(f"清理后数据: {df.shape[0]} 行, {df.shape[1]} 列")
    
    # 保存清理后的文件
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"最终文件已保存到: {output_file}")
    
    return df

def final_text_cleanup(text):
    if pd.isna(text) or text == '':
        return text
    
    text = str(text)
    
    # 1. 移除连续的破折号
    text = re.sub(r'-{3,}', '', text)
    
    # 2. 移除多余的逗号（连续的逗号）
    text = re.sub(r',{2,}', '，', text)
    
    # 3. 移除行首行尾的逗号和空格
    text = re.sub(r'^[,，\s]+|[,，\s]+$', '', text)
    
    # 4. 移除多余的空格
    text = re.sub(r'\s+', ' ', text)
    
    # 5. 如果只剩下标点符号，返回空字符串
    if re.match(r'^[,，.。?？!！;；:：\s]*$', text):
        return ''
    
    return text.strip()

def main():
    input_file = '/Users/jarvis/PycharmProjects/crawler/gooood_gooood-interview_qa_clean_chinese_only.csv'
    output_file = '/Users/jarvis/PycharmProjects/crawler/gooood_gooood-interview_qa_final.csv'
    
    result_df = final_cleanup_csv(input_file, output_file)
    
    # 显示最终结果统计
    print("\n=== 最终清理结果 ===")
    print(f"最终行数: {result_df.shape[0]}")
    print(f"最终列数: {result_df.shape[1]}")
    print(f"列名: {list(result_df.columns)}")
    
    # 显示前几行预览
    print("\n=== 前5行预览 ===")
    for i, row in result_df.head().iterrows():
        print(f"行 {i+1}:")
        for col in result_df.columns:
            if pd.notna(row[col]) and str(row[col]).strip() != '':
                print(f"  {col}: {str(row[col])[:100]}..." if len(str(row[col])) > 100 else f"  {col}: {row[col]}")
        print()
    
    print("最终清理完成！")

if __name__ == "__main__":
    main()