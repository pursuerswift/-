import os
import pandas as pd
import plotly.express as px

# 读取Excel文件
file_path = 'news_wtu.xls'  # 请确保文件路径正确
df = pd.read_excel(file_path, sheet_name='data')

# 将时间列转换为日期格式
df['时间'] = pd.to_datetime(df['时间'])

# 分别统计每个分类每天的新闻发布数量
categories = ['学校新闻', '思想观点', '综合新闻', '学术动态']


for category in categories:
    category_df = df[df['分类'] == category]
    daily_counts = category_df['时间'].value_counts().sort_index()
    daily_counts = daily_counts.reset_index()
    daily_counts.columns = ['日期', '新闻数量']

    # 创建一个散点图
    fig = px.scatter(daily_counts, x='日期', y='新闻数量',
                     labels={'日期': '日期', '新闻数量': '新闻数量'},
                     title=f'{category} 每天发布的新闻数量散点图',
                     hover_data={'日期': '|%Y-%m-%d', '新闻数量': True})

    # 保存图表为HTML文件
    folder_path = '散点图'
    os.makedirs(folder_path, exist_ok=True)
    html_files = []
    html_file_path = os.path.join(folder_path, f'news_scatter_plot_{category}.html')
    fig.write_html(html_file_path)
    html_files.append(html_file_path)

print(f'图表已保存为: {html_files}')
