# coding:utf-8
import urllib2
from bs4 import BeautifulSoup
import sys
import proxyip
import socket
"""
作者：LeonTian
行业：会计
年龄：23
学习编程时间：2016年11月26日至今
介绍项目：
1.完成了网页的解析
2.加入了自动获得代理ip的反爬程序
3.对网页访问超时进行了处理

后续功能：
1.对爬取文章进行数据挖掘与分析
2.生成词云

学习感受：通过这种有时间限制的项目，我对python又有了更多的认识，
对很多模块又有了更多掌握。希望还有更多的这类活动。
"""

reload(sys)
sys.setdefaultencoding('utf-8')


timeout = 20
socket.setdefaulttimeout(timeout)
header= {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept':'ext/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection':'keep-alive',
        'Cookie':'CNZZDATA1256051298=200779990-1488433794-%7C1488433794',
        'host':'www.mkqcdgt.com'
}

# 通过proxyip模块获得代理地址
proxies = proxyip.getListProxies()
# 设定一个代理地址
proxy = proxies[0]

#获得并生成小说目录网址
def get_pagemenu():
    global total_lst
    index_lst = []
    total_lst = []
    # 控制IP爬虫翻页
    ipIndex = 1
    host = 'http://www.mkqcdgt.com/html/'
    # 生成所有板块的板块首页url
    for i in range(34, 41):
        index_lst.append(host + 'part/index%s.html' % str(i))
    for partindex in index_lst:
        try:
            # 加载代理
            proxy = urllib2.ProxyHandler()
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)
            # 通过Post的方式获得页面
            request = urllib2.Request(partindex,headers=header)
            response = urllib2.urlopen(request,timeout=30).read().decode('gb18030')
            # 用BeautifulSoup解析网页，使用html解析器
            soup = BeautifulSoup(response, "html.parser")
            # 寻找页面中标注页码的部分
            pagenum = soup.find(name='div', attrs={
                'class': 'pages'
            })
            total = pagenum.get_text()
            # 通过切片获得总页数，并根据网页规则生成URL
            for num in range(2, int(total.split()[1][2:4]) + 1):
                url = host + "part/index%s" % partindex[-7:-5] + "_%s.html" % num
                total_lst.append(url)
            for index in index_lst:
                total_lst.append(index)
        # 对访问超时的页面进行处理
        except socket.timeout as e:
            print type(e)  # catched
        # IP被封后通过新的代理进行爬取
        except urllib2.HTTPError:
            # 使用爬取的前20页IP代理
            if ipIndex < 20:
                proxy = proxies[ipIndex]
                print '新IP:Port', proxy
                ipIndex += 1

    print total_lst

def get_page_url():
    global hrefs
    ipIndex = 1
    for url in total_lst:
        try:
            # 加载代理
            proxy = urllib2.ProxyHandler()
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)
            # Post访问页面
            request = urllib2.Request(url, headers=header)
            response = urllib2.urlopen(request, timeout=30).read().decode('gb18030')
            soup = BeautifulSoup(response, "html.parser")
            artical_url = soup.find_all(name='a',attrs={
                'target': "_blank"
            })
            hrefs = []
            # 将不是文章页的元素跳过
            for page in artical_url:
                if page.get_text() == "":
                    pass
                else:
                    # 生成文章详情页网址
                    href = 'http://www.mkqcdgt.com' + page.attrs['href']
                    hrefs.append(href)
                    get_novel(href)
        # 对访问超时的处理
        except socket.timeout as e:
            print type(e)  # catched
        # 加载新的代理IP
        except urllib2.HTTPError:
            if ipIndex < 10:
                proxy = proxies[ipIndex]
                print '新IP:Port', proxy
                ipIndex += 1


def get_novel(href):
    ipIndex = 1
    try:
        proxy = urllib2.ProxyHandler()
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
        request = urllib2.Request(href, headers=header)
        response = urllib2.urlopen(request,timeout=20).read().decode('gb18030')
        soup = BeautifulSoup(response, "html.parser")
        # 小说页面有两种形式，用不同的方法进行解析
        novel = soup.find_all(name='div', attrs={
                        'class': "news_content"
                    })
        novel_2 = soup.find_all(name='div', attrs={
                        'color': "#0000FF",
                        'style':"font-size:15px;"
                    })
        # 获得小说标题
        novel_name = soup.find(name='h1')
        text = ""
        # 由于函数不能对None进行操作，要先判断novel是否为None
        if novel is not None:
            for m in novel:
                for i in m.get_text().split():
                    text = text + i + '\r\n'
        if novel_2 is not None:
            for m in novel:
                for i in m.get_text().split():
                    text = text + i + '\r\n'
        text = text.encode('utf-8')
        with open(r"%s.txt" % novel_name.get_text(), 'wb') as f:
            f.write(text)
            print "%s" % novel_name.get_text() + "下载完成"
    except socket.timeout as e:
        print type(e)  # catched
    except urllib2.HTTPError:
        if ipIndex < 10:
            proxy = proxies[ipIndex]
            print '新IP:Port', proxy
            ipIndex += 1



get_pagemenu()
get_page_url()






