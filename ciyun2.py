import xlrd
import jieba
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd

# 加载保存的 Excel 文件
file_path = 'news_wtu.xls'
workbook = xlrd.open_workbook(file_path)
sheet = workbook.sheet_by_name('data')

# 指定中文字体
font_path = 'simsun.ttf'
my_font = fm.FontProperties(fname=font_path)

# 收集所有内容列的文本
all_content = ""
for row_idx in range(1, sheet.nrows):
    content = sheet.cell_value(row_idx, 3)
    all_content += f" {content}"

# 使用jieba进行分词
tokens = jieba.lcut(all_content)
# 去除停用词
stopwords = {'的', '了', '和', '是', '在', '这', '有', '也', '与', '中'}
tokens = [token for token in tokens if token not in stopwords and len(token) > 1]

# 统计词频
word_counts = Counter(tokens)
most_common_words = word_counts.most_common(20)

# 生成词云
word_cloud = WordCloud(
    font_path=font_path,
    background_color='white',
    max_words=2000,
    height=1200,
    width=1600,
    max_font_size=None,
    random_state=40
).generate_from_frequencies(dict(most_common_words))

# 显示词云图像
plt.figure()
plt.imshow(word_cloud, interpolation='bilinear')
plt.title("Top 20 词频", fontproperties=my_font, fontsize=16)
plt.axis('off')
plt.savefig('top_20_words_wordcloud.png', dpi=300)
plt.close()

# 将前20个词汇及其词频导入到一个新的Excel文件中
df = pd.DataFrame(most_common_words, columns=['Word', 'Frequency'])
df.to_excel('top_20_words_frequency.xlsx', index=False)

print("词云图像已保存为 top_20_words_wordcloud.png，词频数据已保存为 top_20_words_frequency.xlsx。")
