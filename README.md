# 几个爬虫练习项目
1. 爬取quotes.toscrape.com名言网信息
2. 爬取天气信息并写出为csv文件、json文件，写出到数据库
3. bing词典，有道词典在线查词
4. 综合练习：爬取拉钩网所有职位信息并写入mysql

## 以下是一些常用操作的笔记

- .py文件头

```
#!/usr/bin/python3
#-*- coding: utf-8 -*-
```
- 指定头信息
```
from urllib.request import Request
# 模拟了使用浏览器在访问
head = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
                "Cookie":"xxxxxxxxxxxxx"}

request = Request(url, headers=head)
response = urlopen(request)

```
- 线程睡眠
```
# 可用于访问过于频繁导致获取页面失败的问题
import time
time.sleep(1)
```
- from urlib.request import urlopen
```
response = urlopen(url)
response.getcode()#返回状态码
html = response.read().decode("utf-8")#获得网页
```

- form urllib.request import urlretrieve
```
#下载一个网页或图片到本地

result=urlretrieve(url="http://****", filename="c:/myfile.html")
```


- from urllib.parse import urlencode
    
```
#把中文进行url编码,（在写bing查词时输入中文也可以查询结果时用到）
urlencode(param)#para是Dict类型
#如果只转换一个字符串就使用quote
```


- #标签选取器
    
```
from bs4 import BeautifulSoup
response = urlopen(url)
bs = BeautifulSoup(response,"html.parser")
lis = bs.select("div.qdef>ul>li")#返回一个列表
```


- #正则表达式的使用

```
import re
response = urlopen(url)
html = response.read().decode("utf-8")
#匹配pos或pos web （.*?）表示非贪婪模式
re.findall('<span class="(pos|pos web)">(.*?)</span>',html)
```

- #去除html标签只保留内容，转换成generator
```
temp = temp_list[i].stripped_strings
temp = "".join(temp)
#  strip 从两边开始搜寻，只要发现某个字符在当前这个方法的范围内，统统去掉
    new_result = single_result.strip("“”.")
```
- #使用get()获取html中的属性值如title
```
direction = two_span_list[0].get("title") + "-" + two_span_list[1].get("title")
```
--------------
- #把一个列表写出到本地的一个csv文件

```
import csv
#使用with open 不用close
with open("c:/weather.csv",mode="w" encoding="utf-8") as f:
    #构造一个csv写出器
    csv_writer = csv.writer(f)
    #写出数据到文件
    csv_writer.writerows(result_list)
```


- 把列表写出成json文件
```
import json
with open("c:/weather3.json", "w", encoding="utf-8") as f:
    json.dump(result_list, f, ensure_ascii=False)
```

    


- 写出数据到数据库
```
#写出到数据库，先安装pymysql模块
import pymysql

#获取连接
con = pymysql.connect(host="loacalhost",user="root",password="123",database="spider",charset="utf-8",port=3306)
#获取游标等同于JDBC中的Statement
cursor = con.cursor()
for record in result_list:
    sql_insert="insert into t_weather (t_data,***) values (%s,%s,****)"
    cursor.excute(sql_insert,record)
con.commit()
cursor.close()
con.close()
```






