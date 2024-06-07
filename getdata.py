import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import xlwt
import time

# 创建一个新的工作簿和工作表
xt = xlwt.Workbook()
xs = xt.add_sheet('data')

# 定义页面和其他变量
pages = [
    {'page': 'xxxw.htm', 'category': '学校新闻'},
            {'page': '/xxxw/318.htm', 'category': '学校新闻'},
            {'page': '/xxxw/317.htm', 'category': '学校新闻'},
            {'page': '/xxxw/316.htm', 'category': '学校新闻'},
            {'page': '/xxxw/315.htm', 'category': '学校新闻'},
            {'page': '/xxxw/314.htm', 'category': '学校新闻'},
            {'page': '/xxxw/313.htm', 'category': '学校新闻'},
            {'page': '/xxxw/312.htm', 'category': '学校新闻'},
            {'page': '/xxxw/311.htm', 'category': '学校新闻'},
    {'page': 'sxgd.htm', 'category': '思想观点'},
            {'page': '/sxgd/32.htm', 'category': '思想观点'},
            {'page': '/sxgd/31.htm', 'category': '思想观点'},
            {'page': '/sxgd/30.htm', 'category': '思想观点'},
            {'page': '/sxgd/29.htm', 'category': '思想观点'},
            {'page': '/sxgd/28.htm', 'category': '思想观点'},
            {'page': '/sxgd/27.htm', 'category': '思想观点'},
            {'page': '/sxgd/26.htm', 'category': '思想观点'},
            {'page': '/sxgd/25.htm', 'category': '思想观点'},
    {'page': 'zhxw1.htm', 'category': '综合新闻'},
            {'page': '/zhxw1/465.htm', 'category': '综合新闻'},
            {'page': '/zhxw1/464.htm', 'category': '综合新闻'},
            {'page': '/zhxw1/463.htm', 'category': '综合新闻'},
            {'page': '/zhxw1/462.htm', 'category': '综合新闻'},
            {'page': '/zhxw1/461.htm', 'category': '综合新闻'},
            {'page': '/zhxw1/460.htm', 'category': '综合新闻'},
            {'page': '/zhxw1/459.htm', 'category': '综合新闻'},
            {'page': '/zhxw1/458.htm', 'category': '综合新闻'},
     {'page': 'xsdt.htm', 'category': '学术动态'},
            {'page': '/xsdt/57.htm', 'category': '学术动态'},
            {'page': '/xsdt/56.htm', 'category': '学术动态'},
            {'page': '/xsdt/55.htm', 'category': '学术动态'},
            {'page': '/xsdt/54.htm', 'category': '学术动态'},
            {'page': '/xsdt/53.htm', 'category': '学术动态'},
            {'page': '/xsdt/52.htm', 'category': '学术动态'},
            {'page': '/xsdt/51.htm', 'category': '学术动态'},
            {'page': '/xsdt/50.htm', 'category': '学术动态'},
]

list_news = []
url = "https://news.wtu.edu.cn/"

# 定义请求会话
session = requests.Session()

# 设置重试策略
retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retries)
session.mount('http://', adapter)
session.mount('https://', adapter)

# 忽略 SSL 验证
requests.packages.urllib3.disable_warnings()

# 定义写入 Excel 的函数
def write_to_excel(news_list, sheet):
    # 写入列名
    sheet.write(0, 0, '分类')
    sheet.write(0, 1, '标题')
    sheet.write(0, 2, '时间')
    sheet.write(0, 3, '内容')

    for i, news in enumerate(news_list):
        sheet.write(i + 1, 0, news['category'])
        sheet.write(i + 1, 1, news['title'])
        sheet.write(i + 1, 2, news['time'])
        sheet.write(i + 1, 3, news['content'])

# 获取新闻内容的函数
def get_news_content(link):
    retries = 5
    while retries > 0:
        try:
            res = session.get(link, verify=False)
            res.encoding = res.apparent_encoding
            doc = BeautifulSoup(res.text, 'html.parser')
            content_div = doc.find('div', class_='v_news_content')
            return content_div.get_text(strip=True) if content_div else '未找到内容'
        except requests.RequestException as e:
            print(f"获取页面 {link} 出现异常: {e}")
            retries -= 1
            if retries == 0:
                print(f"获取页面 {link} 失败，已达到最大重试次数。")
            time.sleep(5)
    return '获取内容失败'

# 遍历每个页面以收集标题和发布时间
for p in pages:
    urlt = url + p['page']
    retries = 5  # 设置重试次数
    while retries > 0:
        try:
            res = session.get(urlt, verify=False)
            res.encoding = res.apparent_encoding
            doc = BeautifulSoup(res.text, 'html.parser')
            listp = doc.find_all('li', id=lambda x: x and x.startswith('line_u'))

            for item in listp:
                title_tag = item.find('a')
                time_tag = item.find('span', class_='time')
                if title_tag and time_tag:
                    news_title = title_tag.text.strip()
                    news_time = time_tag.text.strip()
                    news_link = url + title_tag['href']
                    news_content = get_news_content(news_link)
                    list_news.append({'category': p['category'], 'title': news_title, 'time': news_time, 'link': news_link, 'content': news_content})

            # 跳出重试循环
            break

        except requests.RequestException as e:
            print(f"获取页面 {urlt} 出现异常: {e}")
            retries -= 1
            if retries == 0:
                print(f"获取页面 {urlt} 失败，已达到最大重试次数。")
            time.sleep(5)  # 等待5秒再重试

# 写入Excel表格
write_to_excel(list_news, xs)

# 保存Excel文件
file_path = 'news_wtu.xls'
xt.save(file_path)

print(f'爬取完成！数据保存在 {file_path}')
