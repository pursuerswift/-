import os
import pandas as pd
import plotly.express as px

# 读取Excel文件
file_path = 'news_wtu.xls'
df = pd.read_excel(file_path, sheet_name='data')

# 将时间列转换为日期格式
df['时间'] = pd.to_datetime(df['时间'])

# 统计每天的新闻发布数量
daily_counts = df['时间'].value_counts().sort_index()
daily_counts = daily_counts.reset_index()
daily_counts.columns = ['日期', '新闻数量']

# 创建一个散点图
fig = px.scatter(daily_counts, x='日期', y='新闻数量',
                 labels={'日期': '日期', '新闻数量': '新闻数量'},
                 title='每天发布的新闻数量散点图',
                 hover_data={'日期': '|%Y-%m-%d', '新闻数量': True})

# 保存图表为HTML文件
folder_path = '散点图'
html_file_path = os.path.join(folder_path, 'news_scatter_plot.html')
fig.write_html(html_file_path)

print(f'图表已保存为 {html_file_path}')
