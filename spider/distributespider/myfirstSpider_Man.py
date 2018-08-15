from myfirstSpider_DataOutput import DataOutput
#from myfirstSpider_HtmlDownloader import HtmlDownloader
#from myfirstSpider_HtmlParser import HtmlParser
from myfirstSpider_URLManager import UrlManager

class SpiderMan(object):

    def __init__(self):
        self.manager = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()

    def crawl(self,root_url):
        '''
        添加入口URL

        :param root_url:
        :return:
        '''
        #add in URL
        self.manager.add_new_url(root_url)
        #判断url管理器中是否有新的url，同时判断抓取了多少url
        while(self.manager.has_new_url() and self.manager.old_url_size()<100):
            try:
                #从URL管理器中获取新的URL
                new_url = self.manager.get_new_url()
                print("get url succeful")
                #HTML下载网页
                html = self.downloader.download(new_url)
                print("download over")
                #HTML解析器抽取数据
                mew_urls,data = self.parser.parser(new_url,html)
                print("parser over")
                #将抽取的数据放入URL管理器中
                self.manager.add_new_urls(mew_urls)
                print("save uls over")
                #数据存储器存储文件
                self.output.store_data(data)
                print("已经抓取%s 个链接"%self.manager.old_url_size())
                print("未抓取%s 个链接" % self.manager.new_url_size())
            except Exception as e:
                print("crawl failed")
                print(e)
            #数据存储器将文件输出成制定格式

        self.output.output_html()

if __name__=="__main__":
    spider_man = SpiderMan()
    spider_man.crawl()"https://baike.baidu.com/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB"