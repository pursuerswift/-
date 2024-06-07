    此次课程设计主要统计武汉纺织大学新闻网站下学校新闻、思想观点、综合新闻和学术动态的新闻数据，包括标题，发布时间，正文内容。网站网址为武汉纺织大学新闻文化网 (wtu.edu.cn) 。 这次项目是基于python3.12的数据分析可视化项目。爬取数据部分使用request、BeautifulSoup等相关库，以获得相关数据，使用Excel进行存储。数据可视化部分使用的是pyecharts、jieba等库，进而生成词云以及散点图等html文件。
    爬取代码存放在getdata.py
    生成词云代码存放在ciyun.py和ciyun2.py
    绘制散点图代码存放在drawdata.py和drawdata2.py
    爬取数据存放在news_wtu.xls，
    注意运行程序需提前安装好相关库，如requests，xlwt，jieba，WordCloud，pandas，plotly等
