#!/usr/bin/python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen as open

import re

url = "http://quotes.toscrape.com/"

response = open(url)

html = response.read()
html = html.decode("UTF-8")


#  获取 10  个  名言
result = re.findall('<span class="text" itemprop="text">(.*)</span>', html)
print(result)
print(len(result))
true_quotes = []
for single_result in result:
    #  strip 从两边开始搜寻，只要发现某个字符在当前这个方法的范围内，统统去掉
    new_result = single_result.strip("“”.")
    true_quotes.append(new_result)
    # print(new_result)


# 获取 10 个名言的作者
true_authors = []
authors = re.findall('<small class="author" itemprop="author">(.*)</small>', html)
print(len(authors))
for author in authors:
    true_authors.append(author)

#使用非贪婪模式匹配
tagss = re.findall('<div class="tags">(.*?)</div>', html, re.RegexFlag.DOTALL)
print(tagss)
print(len(tagss))
tag_result = []
for tag in tagss:
    tag_temp = re.findall('<a class="tag" href="(.*)">(.*)</a>', tag)
    # print(tag_temp)
    # tag1,tag2,tag3
    tag_t1 = []
    for tag in tag_temp:
        # print(tag[1])
        tag_t1.append(tag[1])
    # print("---------------")
    tag_str = ",".join(tag_t1)
    tag_result.append(tag_str)

for i in range(10):
    print("\t".join([true_quotes[i], true_authors[i], tag_result[i]]))

