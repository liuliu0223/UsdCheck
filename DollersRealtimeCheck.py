import datetime
import os
import requests
from bs4 import BeautifulSoup

# 目标网页的URL
url = 'https://www.5waihui.com/'
logFile = 'log.txt'
wholepath = 'C:\\Users\\user\\Desktop\\APP\\log.txt'
print(f"路径名称：{os.path.dirname(wholepath)}\n")
# 发送HTTP请求以获取网页内容
response = requests.get(url)
web_content = response.content

# 使用BeautifulSoup解析网页内容
soup = BeautifulSoup(web_content, 'html.parser')

# 定位到美元汇率数据所在的表格
# 根据提供的网页结构，我们假设美元汇率位于表格的第一行第二列
table = soup.find('table')
rows = table.find_all('tr')

today = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
print(f'日期：{today}')

text = ""
if len(rows)<0:
    print(f'没有外币数据！')
else:
    usd_titles = rows[0].find_all('b')  # 标题行
    it2 = 1
    while it2 < len(rows):
        usd_rates = rows[it2].find_all('td')
        # 提取并打印美元的现汇买入价和现汇卖出价
        it3 = 0
        while it3 < len(usd_rates):
            cashtitle_name = usd_titles[it3].get_text()
            cashs = usd_rates[0].get_text()
            if cashs.find('美元') > -1:
                usd_buy_rate = usd_rates[it3].get_text()
                print(f"{cashtitle_name}: {usd_buy_rate}")
                text += cashtitle_name + ':' + usd_buy_rate + '\n'
            it3 += 1
        it2 += 1
with open(wholepath, 'r', encoding='utf-8') as file:
    original_content = file.read()
    file.close()
# 将日志信息插入到文件内容的前面
new_content = text + original_content

os.chmod(wholepath, 0o666)
with open(wholepath, 'w', encoding='utf-8') as file:
    file.write(f"\n日期：{today}\n{new_content}")
    file.close()