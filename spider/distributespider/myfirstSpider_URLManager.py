#coding:utf-8
import _compat_pickle
import hashlib
class UrlManager(object):
    def __init__(self):
        #self.new_urls = set()
        #self.old_urls = set()
        self.new_urls = self.load_progress('new_urls.txt')#未爬取的url集合
        self.old_urls = self.load_progress('old_urls.txt')#已爬取的URL集合

    def has_new_url(self):
        '''
        判断是否有未爬取的URL
        :return:
        '''
        return self.new_url_size() != 0

    def get_new_url(self):
        '''
        获取一个未爬取的URL
        :return:
        '''
        new_url = self.new_urls.pop()
        m = hashlib.md5()
        m.update(new_url.encode("utf8"))
        self.old_urls.add(m.hexdigest()[8:-8])
        return new_url

    def add_new_url(self,url):
        '''
        将新的URL添加到未爬取的URL集合中
        :return:
        '''
        if url is None:
            return
        m = hashlib.md5()
        m.update(url.encode("utf8"))
        url_md5 = m.hexdigest()[8:-8]
        if url not in self.new_urls and url_md5 not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self,urls):
        '''
        将新的URLs添加到未爬取的URL集合中
        ：param urls :url 集合
        :param urls:
        :return:
        '''
        if urls is None or len(urls)== 0 :
            return
        for url in urls:
            self.add_new_url(url)

    def new_url_size(self):
        '''
        获取url集合大小
        :return:
        '''
        return len(self.new_urls)

    def old_url_size(self):
        '''
        获取已经爬取的URL集合的大小
        :return:
        '''
        return len(self.old_urls)
    def save_progress(selfs,path,data):
        '''

        :param path:文件路径
        :param data: 数据
        :return:
        '''
        with open(path,'wb') as f:
            _compat_pickle.dump(data,f)

    def load_progress(self,path):
        '''
        从本地加载文件进度
        :param path: 文件路径
        :return: 返回set集合
        '''
        print('[+] 从文件加载进度: %s'%path)
        try:
            with open(path,'rb') as f:
                tmp = _compat_pickle.load(f)
                return tmp
        except:
            print('[!]无进度文件，创建：%s'%path)
        return set()
