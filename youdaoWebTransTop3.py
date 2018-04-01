#!/usr/bin/python3
#-*- coding: utf-8 -*-
from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
'''
提取有道词典网络翻译的前3个结果
'''
def youdaofanyi(key):
    key = quote(key)
    url="http://dict.youdao.com/w/eng/"+key
    print(url)
    response = urlopen(url)
    bs = BeautifulSoup(response,"html.parser")
    #选取网络翻译的条目
    lis = bs.select("div#tWebTrans > div.wt-container > div.title > span")
    result=[]
    n=0
    for li in lis:
        n+=1
        if n>3:
            break
        li = li.stripped_strings
        li = "".join(li)
        result.append(li)
    re = ";".join(result)
    print(re)
while True:
    key = input("please input you key : ")
    if key == 'bye' or key == 'quit':
        break
    youdaofanyi(key)