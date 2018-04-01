from  urllib.request import urlopen
from bs4 import BeautifulSoup

url = "http://quotes.toscrape.com/"

# 模拟用户发起了一个URL连接的访问
response = urlopen(url)

# 初始化一个 bs 实例
#  对应的response对象的解析器， 最常用的解析方式，就是默认的  html.parser
bs  = BeautifulSoup(response,"html.parser")


spans = bs.select("span.text")
# print(spans)
# print(len(spans))
true_quotes = []
for span in spans:
    span_text = span.text
    span_text = span_text.strip("“”")
    true_quotes.append(span_text)
    # print(span_text)
    # print(span)


true_author  = []
authors = bs.select("small.author")
for author in authors:
    true_author.append(author.text)

tags = bs.select("div.tags")
true_tags = []
for tag in tags:
    # print(type(tag))
    tag_a = tag.select("a.tag")
    tag_list = [tag_aa.text for tag_aa in tag_a]
    true_tags.append(",".join(tag_list))
    # print(tag_list)


for i in range(len(true_quotes)):
    print("\t".join([true_quotes[i], true_author[i], true_tags[i]]))