# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 18:34:23 2018

@author: imliu
"""
from urllib.request import urlopen
import feedparser

# Download the RSS feed and parse it
try:
    u = urlopen('http://store.steampowered.com/feeds/weeklytopsellers.xml')
except:
    print('Download the RSS Error!')
d = feedparser.parse(u)


# Extract the information we need.
title = d.feed.title
subtitle = d.feed.subtitle
pubdata = d.feed.published

gameli = []

for g in d.entries:
    game = {}
    game['no'] = g['title'][1:3].strip()
    game['name'] = g['title'][5:].strip()
    game['link'] = g['link']
    # print(game)
    gameli.append(game)

# Save to file
filename = 'SteamTopSellers.txt'
with open(filename, 'a+', encoding='utf-8') as f:
    f.write('\n' + title + '\n' + subtitle + '\n' + pubdata + '\n\n')
    for game in gameli:
        f.write('{} \t {} \t {} \n'.format(
                game['no'], game['name'], game['link']))
