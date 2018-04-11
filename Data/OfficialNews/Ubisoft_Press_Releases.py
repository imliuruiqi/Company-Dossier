import requests
import time
from bs4 import BeautifulSoup


def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        print('Get html Error.')
        return " ERROR "


def get_content(url):
    '''
    分析网页文件，整理出新闻的主要信息（标题、摘要、日期、作者），并保存在列表变量中
    '''
    news = []
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')

    # 找到文章的列表
    #ultag = soup.find('ul',attrs={'class': 'press-articles-list'})
    litags = soup.find_all('li')

    # 通过循环获取到所需的文章信息
    for li in litags:
        article = {}  # 初始化字典存储文章信息
        try:
            article['title'] = li.find(
                'a', attrs={'id': 'social-link'}).text.strip()
            article['date'] = li.find(
                'div', attrs={'class': 'date'}).text.strip()
            article['link'] = li.find(
                'a', attrs={'id': 'social-link'})['href']
            article['desc'] = li.find(
                'div', attrs={'class': 'desc'}).a.text.strip()
            news.append(article)
        except:
            print('内容筛选出现一个小错误')
    return news


def save2file(dict):
    '''
    将爬取的信息存在本地的当前目录的同名文件中 
    '''
    #filename = 'Ubisoft_Press_Releases.txt'

    with open('Ubisoft_Press_Releases.txt', 'a+', encoding='utf-8') as f:
        for article in dict:
            f.write('标题：{} \t 摘要：{} \t 链接：{} \t 日期：{} \n'.format(
                article['title'], article['desc'], article['link'], article['date']))
        print('当前页面爬取完成')


def main(base_url, deep):
    url_list = []

    for i in range(0, deep):
        url_list.append(base_url + str(i) + '?locale=en-US')
    print('已准备好带爬取网址列表')

    # 写入数据
    for url in url_list:
        content = get_content(url)
        save2file(content)
    print('所有信息已保存完毕。')


# main
base_url = 'https://ubigroup-api.ubisoft.com/PressRelease/GetList/20/'
deep = 3
if __name__ == '__main__':
    main(base_url, deep)
input("Press any key to exit")
