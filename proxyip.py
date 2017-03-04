# coding:utf-8
import requests
from bs4 import BeautifulSoup
import re
import os.path

# 构造Header
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)'
headers = {'User-Agent': user_agent}

# 爬取代理
def getListProxies():
    # 获得页面
    session = requests.session()
    page = session.get("http://www.xicidaili.com/nn", headers=headers)
    # soup解析
    soup = BeautifulSoup(page.text, 'lxml')
    proxyList = []
    taglist = soup.find_all('tr', attrs={'class': re.compile("(odd)|()")})
    # 构造代理信息
    for trtag in taglist:
        tdlist = trtag.find_all('td')
        proxy = {'http': tdlist[1].string + ':' + tdlist[2].string,
                 'https': tdlist[1].string + ':' + tdlist[2].string}
        url = "http://ip.chinaz.com/getip.aspx"  # 用来测试IP是否可用的url
        # 测试IP是否可用
        try:
            response = session.get(url, proxies=proxy, timeout=5)
            proxyList.append(proxy)
            if (len(proxyList) == 10):
                break
        except Exception, e:
            continue

    return proxyList

print getListProxies()