import xlrd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 加载保存的 Excel 文件
file_path = 'news_wtu.xls'
workbook = xlrd.open_workbook(file_path)
sheet = workbook.sheet_by_name('data')

# 指定中文字体
font_path = 'simsun.ttf'
my_font = fm.FontProperties(fname=font_path)

# 初始化词云参数
word_clouds = {}

# 处理每一行并构建每个分类的文本
for row_idx in range(1, sheet.nrows):
    category = sheet.cell_value(row_idx, 0)
    title = sheet.cell_value(row_idx, 1)
    content = sheet.cell_value(row_idx, 3)

    # 组合标题和内容以便更好地表现
    text = f"{title} {content}"

    # 使用jieba进行分词
    tokens = jieba.lcut(text)
    processed_text = " ".join(tokens)

    # 添加到相应的分类中
    if category not in word_clouds:
        word_clouds[category] = processed_text
    else:
        word_clouds[category] += " " + processed_text

# 生成并保存词云图像
for category, text in word_clouds.items():
    word_cloud = WordCloud(
        font_path=font_path,
        background_color='white',
        max_words=2000,
        height=1200,
        width=1600,
        max_font_size=100,
        random_state=40,
        stopwords={'的', '了', '和', '是', '在', '这', '有', '也', '与', '中'}
    ).generate(text)

    plt.figure()
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.title(category, fontproperties=my_font, fontsize=16)
    plt.axis('off')
    plt.savefig(f'{category}_wordcloud.png', dpi=300)  # 增加 dpi 参数以提高保存图片的清晰度
    plt.close()  # 关闭图表，释放内存

plt.show()
