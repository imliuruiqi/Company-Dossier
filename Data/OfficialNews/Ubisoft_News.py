import requests
import json


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
    news = []
    html = get_html(url)
    try:
        articleli = json.loads(html)
        for article in articleli:
            news.append(article)
        print('内容筛选完成。')
    except:
        print('内容筛选出现错')
    return news


def save2file(dict):
    '''
    将爬取的信息存在本地的当前目录的同名文件中 
    '''
    with open('Ubisoft_News.txt', 'a+', encoding='utf-8') as f:
        for article in dict:
            f.write('标题：{} \t 时间：{} \t 内容：{} \n'.format(
                article['title'], article['date'], article['content']))


def main(base_url, deep):
    url = base_url + str(deep*10)
    print('已准备好待爬取网站地址：' + url)
    content = get_content(url)
    save2file(content)
    print('所有信息已保存完毕。')


# main
base_url = 'https://news-api.ubisoft.com/v1/en-us/articles/latest?limit='
deep = 2
if __name__ == '__main__':
    main(base_url, deep)
input("Press any key to exit")
