# -*- coding: utf-8 -*-
"""
抓取steam上Ubisoft发行的游戏列表，获取其发行日期，评价等信息。
"""
import requests
from bs4 import BeautifulSoup


def get_html(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Host': 'store.steampowered.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36', }
    try:
        r = requests.get(url, timeout=300, headers=headers)
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
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')

    # 查找游戏信息的标签列表
    atags = soup.find_all('a', attrs={
        'class': 'search_result_row ds_collapse_flag'})

    # 初始化游戏信息列表
    gameli = []
    # 使用循环语句将游戏的名称、发行日期和评价信息筛选出来，并存在gameli列表
    for tag in atags:
        game = {}
        # 获取游戏名称和发行日期
        game['title'] = tag.find('span', attrs={
            'class': 'title'}).text.strip()
        game['releasedata'] = tag.find('div', attrs={
            'class': 'col search_released responsive_secondrow'}).text.strip()

        # 由于部分游戏无评价，将其对应属性值设为None
        try:
            game['reviewscore'] = tag.find('div', attrs={
                'class': 'col search_reviewscore responsive_secondrow'}).span['class'][1]
            game['reviews'] = tag.find('div', attrs={
                'class': 'col search_reviewscore responsive_secondrow'}).span['data-tooltip-html'].strip()
        except:
            game['reviewscore'] = None
            game['reviews'] = None
            print('Something happened.')

        gameli.append(game)

    return gameli


def save2file(dict):
    '''
    将爬取的信息存在本地的当前目录的同名文件中 
    '''
    filename = 'steamgameinfo.txt'
    with open(filename, 'a+', encoding='utf-8') as f:
        for game in dict:
            try:
                review = game['reviews'].partition('<br>')
                f.write('名称：{} \t 发行日期：{} \t 评级：{} \t 评价详情：{} \n'.format(
                        game['title'], game['releasedata'], review[0], review[2]))
            except:
                f.write('名称：{} \t 发行日期：{} \t 评级：{} \t 评价详情：{} \n'.format(
                        game['title'], game['releasedata'], game['reviews'], game['reviews']))
        print('当前页面爬取完成')


def main(base_url, deep):
    url_list = []

    for i in range(1, deep+1):
        url_list.append(base_url + str(i))
    print('已准备好待爬取网址列表')

    for url in url_list:
        gamelist = get_content(url)
        save2file(gamelist)
    print('所有信息已保存完毕。')


# 主程序
base_url = 'http://store.steampowered.com/search/?sort_by=Released_DESC&publisher=Ubisoft&page='
deep = 17
if __name__ == '__main__':
    main(base_url, deep)
input("Press any key to exit")
