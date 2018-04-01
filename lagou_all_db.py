#!/usr/bin/python3
# -*- coding: utf-8 -*-
# author: https://blog.csdn.net/zhongqi2513


from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup
import time
import pymysql


"""
爬取拉勾网所有招聘信息并存入mysql数据库


数据库建表语句：

create database if not exists spider;
use spider;
CREATE TABLE `lagou` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `t_job` varchar(255) DEFAULT NULL,
  `t_addr` varchar(255) DEFAULT NULL,
  `t_tag` varchar(255) DEFAULT NULL,
  `t_com` varchar(255) DEFAULT NULL,
  `t_money` varchar(255) DEFAULT NULL,
  `t_edu` varchar(255) DEFAULT NULL,
  `t_exp` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
show tables;
select * from lagou;


"""


# 模拟了使用浏览器在访问
head = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
                "Cookie":"_ga=GA1.2.572475695.1522203171; user_trace_token=20180328101310-8faca567-322d-11e8-a23e-525400f775ce; LGSID=20180328101310-8faca6f5-322d-11e8-a23e-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGUID=20180328101310-8faca856-322d-11e8-a23e-525400f775ce; _gid=GA1.2.917932989.1522203171; index_location_city=%E5%8C%97%E4%BA%AC; JSESSIONID=ABAAABAAAIAACBICD5501D7E1D8273C03AFB6704807496B; TG-TRACK-CODE=index_navigation; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1522203691; X_HTTP_TOKEN=483c5dc38a3823a6b6b0f4fee4873734; _gat=1; SEARCH_ID=beab97953e78487eb14fe25a9ed9e141; LGRID=20180328102808-a7093390-322f-11e8-b652-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1522204069"}


con = pymysql.connect(host="localhost", user="root", password="123", database="spider", charset='utf8', port=3306)
cursor = con.cursor()

# [jobs[i],addrs[i],companys[i],true_tags[i],moneys[i],edus[i],exps[i]]
lagou_insert_sql = "insert into lagou (t_job, t_addr, t_com, t_tag, t_money, t_edu, t_exp) VALUES (%s, %s, %s, %s, %s, %s, %s)"


# 获取所有职业类型的URL
def get_all_url():
    url = "https://www.lagou.com/"
    request1 = Request(url, headers=head)
    response = urlopen(request1)
    bs = BeautifulSoup(response, "html.parser")
    url_list_a = bs.select("div.menu_sub a")
    url_list = [url.get("href") for url in url_list_a]
    url_list.remove("https://www.lagou.com/zhaopin/C%23/")
    # print(len(url_list))
    # print(url_list)

    return url_list




'''
https://www.lagou.com/zhaopin/Java/
'''
def crawl(link):

    print("正在爬取的URL ： %s" % link)
    # link = "https://www.lagou.com/zhaopin/C%23/"

    page = 1
    # 获取这个link锁对应的所有页数
    while True:
        time.sleep(0.5)

        # 当前的这个URL会是涉及分页的。
        new_link = link + str(page)

        request = Request(new_link, headers=head)
        temp = 1
        try:
            url_response = urlopen(request)
            url_bs = BeautifulSoup(url_response, "html.parser")
        except:
            temp = 2
        else:
            job_list = url_bs.select("ul.item_con_list li h3")
            jobs = [job_h3.text for job_h3 in job_list]
            if len(jobs) == 0:
                break

            #  正常的逻辑处理
            addrs = url_bs.select("span.add em")
            addrs = [addr.text for addr in addrs]

            companys = url_bs.select("div.company_name a")
            companys = [c.text for c in companys]

            tagss = url_bs.select("div.list_item_bot div.li_b_l")
            true_tags = []
            for tags in tagss:
                spans = tags.select("span")
                tag_content = ",".join([span.text for span in spans])
                true_tags.append(tag_content)

            moneys = url_bs.select("span.money")
            moneys = [money.text for money in moneys]

            exps_and_edus = url_bs.select("div.p_bot div.li_b_l")
            exps_and_edus = [ee.text.strip() for ee in exps_and_edus]
            edus = [edu.split(" / ")[1] for edu in exps_and_edus]
            expss = [edu.split(" / ")[0] for edu in exps_and_edus]
            exps = [exp.split("\n")[1] for exp in expss]

            print("     爬取第  %d 页成功" % page)
            # print(exps_and_edus)
            # print(edus)
            # print(exps)

            ##  取出的值： jobs    addrs    companys     true_tags     moneys     edus   exps

            for i in range(len(jobs)):
                record = [jobs[i],addrs[i],companys[i],true_tags[i],moneys[i],edus[i],exps[i]]
                #lagou_insert_sql = "insert into lagou (t_job, t_addr, t_com, t_tag, t_money, t_edu, t_exp) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                # print("\t".join([jobs[i],addrs[i],companys[i],true_tags[i],moneys[i],edus[i],exps[i]]))
                cursor.execute(lagou_insert_sql, record)

            con.commit()

            page += 1
        finally:
            if temp == 2:
                break




# 遍历所有职业类型的URL 来获取这个职业类型中的所有 招聘信息
def main():
    link_list = get_all_url()
    for link in link_list:
        crawl(link)

    cursor.close()
    con.close()

main()






