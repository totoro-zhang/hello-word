#coding:utf-8
import requests


class HtmlDownloader(object):
    def download(self,url):
        if url is None:
            return None
        user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        headers = {'User-Agent': user_agent}
        r = requests.get(url,headers = headers)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            print("loader succeful")
            return r.text
        print(r.status_code)
        return None
