from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlencode

'''
使用bing词典查单词案例
'''

def fanyi(key):
    # key = "desk"
    # url = "https://cn.bing.com/dict/search?q=desk"

    param = {"q":key}
    newkey = urlencode(param)
    url = "https://cn.bing.com/dict/search?" + newkey

    response = urlopen(url)
    bs = BeautifulSoup(response, "html.parser")

    # html = response.read().decode("UTF-8")
    # print(html)

    lis = bs.select("div.qdef > ul > li")

    li_content = []
    for li in lis:
        li_content.append(li.text)
        # print(li)
    print(li_content)



while True:
    key = input("please input you key : ")
    if key == 'bye' or key == 'quit':
        break
    fanyi(key)


