from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import urlparse

class ImgCrawler:
    def __init__(self,searchlink = None):
        self.link = searchlink
        self.soupheader = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        self.scrolldown = None
        self.jsdriver = None

    def getPhantomJSDriver(self):
        self.jsdriver = webdriver.Chrome()
        self.jsdriver.get(self.link)

    def scrollDownUsePhatomJS(self, scrolltimes = 1, sleeptime = 10):
        for i in range(scrolltimes):
           self.jsdriver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
           time.sleep(sleeptime)

    def getSoup(self, parser=None):
        print 'a', self.jsdriver.page_source
        return BeautifulSoup(self.jsdriver.page_source, parser)

    def getActualUrl(self, soup=None):
        actualurl = []
        r = re.compile(r"/imgres\?imgurl=")
        for a in soup.find_all('a', href=r):
            parsed = urlparse.urlparse(a['href'])
            url = urlparse.parse_qs(parsed.query)['imgurl']
            actualurl.append(url)
            print url
        return actualurl


if __name__ == '__main__':
    search_url = "https://www.google.com.hk/search?safe=strict&hl=zh-CN&site=imghp&tbm=isch&source=hp&biw=&bih=&btnG=Google+%E6%90%9C%E7%B4%A2&q="
    queryword = raw_input()
    query = queryword.split()
    query = '+'.join(query)
    weblink = search_url + query
    img = ImgCrawler(weblink)
    img.getPhantomJSDriver()
    img.scrollDownUsePhatomJS(2,5)
    soup = img.getSoup('html.parser')
    print weblink
    print soup
    actualurllist = img.getActualUrl(soup)
    print len(actualurllist)
