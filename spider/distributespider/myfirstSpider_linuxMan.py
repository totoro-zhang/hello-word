#!/usr/bin/env python

import random,time
from multiprocessing.managers import BaseManager
from myfirstSpider_DataOutput import DataOutput
from myfirstSpider_URLManager import UrlManager
from multiprocessing import Process
from multiprocessing import Queue


class NodeManager(object):
    '''

    '''
    def start_Manager(self,url_q,result_q):
        '''
        创建分布式管理器
        :param url_q: URL队列
        :param result_q: 结果队列
        :return:
        '''
        #把创建的两个队列注册在网络上，利用register方法，callable参数关联了Queue对象，
        #将Queue对象在网络中暴露
        BaseManager.register('get_task_queue',callable = lambda:url_q)
        BaseManager.register('get_result_queue',callable=lambda:result_q)
        #绑定端口8001，设置验证口令"baike".这个相当于对象初始化
        manager = BaseManager(address=('127.0.0.1',8001),authkey=b'baike')
        return manager
    def url_manager_proc(self,url_q,conn_q,root_url):
        '''

        :param url_q:
        :param conn_q:
        :param root_url:
        :return:
        '''
        url_manager = UrlManager()
        url_manager.add_new_url(root_url)
        while True:
            while(url_manager.has_new_url()):
                #从URL管理器获取新的URL
                new_url = url_manager.get_new_url()
                #将新的URL发送给工作节点
                url_q.put(new_url)
                print('old_url=',url_manager.old_url_size())
                #加一个判断条件，当爬取2000个链接后就关闭，并保存进度
                if(url_manager.old_url_size()>20000):
                     #通知爬虫节点工作结束
                     url_q.put('end')
                     print('control node is over')
                    #关闭管理节点，同时存储set状态
                     url_manager.save_progress('new_urls.txt',url_manager.new_urls)
                     url_manager.save_progress('old_urls.txt',url_manager.old_urls)
                     return
            try:
                if not conn_q.empty():
                    urls = conn_q.get()
                    url_manager.add_new_urls(urls)
            except BaseException:
                time.sleep(0.1)
    def result_solve_proc(self,result_q,conn_q,store_q):
        while(True):
            try:
                if not result_q.empty():
                    content = result_q.get(True)
                    if content['new_urls']=='end':
                        #结果分析进程接收通知然后结束
                        print('结果分析进程接收通知然后结束：')
                        store_q.put('end')
                        return
                    print("result_solve_proc")
                    print(content['new_urls'])
                    conn_q.put(content['new_urls'])#URL为set类型
                    store_q.put(content['data'])
                else:
                    time.sleep(0.1)
            except BaseException:
                time.sleep(0.1)
    def store_proc(self,store_q):
        '''

        :param self:
        :param store_q:
        :return:
        '''
        output = DataOutput()
        while True:
            if not store_q.empty():
                data = store_q.get()
                if data == 'end':
                    print('存储进程接收通知然后结束')
                    output.output_end(output.filepath)
                    return
                output.store_data(data)
            else:
                time.sleep(0.1)
if __name__ == "__main__":
    url_q = Queue()
    result_q = Queue()
    conn_q = Queue()
    store_q = Queue()

    node = NodeManager()
    manager = node.start_Manager(url_q,result_q)
    url_manager_proc = Process(target = node.url_manager_proc,args=(url_q,conn_q,"https://baike.baidu.com/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB"))
    result_solve_proc = Process(target=node.result_solve_proc,args=(result_q,conn_q,store_q))
    store_proc = Process(target=node.store_proc,args=(store_q,))

    #启动三个进程和分布式管理器
    url_manager_proc.start()
    result_solve_proc.start()
    store_proc.start()
    manager.get_server().serve_forever()



