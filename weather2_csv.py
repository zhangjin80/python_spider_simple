from urllib.request import urlopen
from bs4 import  BeautifulSoup
import csv

'''
查询天气信息并保持存csv文件
'''
url = "http://www.weather.com.cn/weather/101010100.shtml"

response = urlopen(url)

bs = BeautifulSoup(response, "html.parser")

# 按照顺序依次找出五列数据：   日期date， 描述 desc,  温度temp    风向direction  level 风力
date_list = bs.select("li > h1")
desc_list = bs.select("li > p.wea")
temp_list = bs.select("li > p.tem")
direction_list = bs.select("li > p.win > em")
level_list = bs.select("li > p.win > i")

result_list = []
for i in range(len(date_list)):
    date = date_list[i].text
    desc = desc_list[i].text
    temp = temp_list[i].stripped_strings
    temp = "".join(temp)
    direction_temp = direction_list[i]
    two_span_list = direction_temp.select("span")
    direction = two_span_list[0].get("title") + "-" + two_span_list[1].get("title")
    level = level_list[i].text
    result_list.append([date, desc, temp,direction,level])
    # print(date, desc, temp,direction,level, sep="\t")
    # resultList


for result in result_list:
    print("\t".join(result))

# # 打开一个文件，进行数据的写入准备
# f = open("c:/weather.csv", mode="w", encoding="utf-8")
# # 构造一个 CSV格式的  写出器
# csv_writer = csv.writer(f)
# # 写出数据
# csv_writer.writerows(result_list)
# f.close()


with open("c:/weather1.csv", mode="w", encoding="utf-8") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerows(result_list)