# import gevent
# from gevent import monkey
# monkey.patch_all()
import aiohttp
from storage import MysqlClient
import asyncio

import time

class Tester():
    def __init__(self):
        self.VALID_STATUS_CODES = [200]
        self.TEST_URL = "https://www.baidu.com"
        self.BATCH_TEST_SIZE = 100
        self.mysql = MysqlClient()

    async def single_proxy_handler(self,proxy):
        """单个代理获取测试"""
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy,bytes):
                    proxy = proxy.decode("utf-8")
                real_proxy = 'http://' + proxy
                print("正在测试",proxy)
                async with session.get(self.TEST_URL,proxy=real_proxy,timeout=15) as response:
                    if response.status in self.VALID_STATUS_CODES:
                        self.mysql.max(proxy)
                        print("代理可用",proxy)
                    else:
                        self.mysql.decrease(proxy)
                        print("请求响应码不合法",proxy)
            except Exception:
                self.mysql.decrease(proxy)
                print("代理请求失败", proxy)
    def run(self):
        try:
            proxy_list = self.mysql.all()
            loop = asyncio.get_event_loop()  # 构建事件循环
            for i in range(0,len(proxy_list),100):
                test_proxies = proxy_list[i:i+self.BATCH_TEST_SIZE]
                tasks = [self.single_proxy_handler(proxy[0]) for proxy in test_proxies] # 构建任务列表
                loop.run_until_complete(asyncio.wait(tasks)) # 将任务列表注入事件循环
                time.sleep(5)
        except Exception:
            print("测试错误")









# import requests

# from multiprocessing import Pool


# class Tester():
#     def __init__(self):
#         self.proxiespool = MysqlClient()
#         self.TEST_URL = "http://www.baidu.com/"
#         self.VALID_STATUS_CODES = [200]
#         # self.pool = Pool(4)
#         self.headers = {
#             'User - Agent': 'Mozilla/5.0(Windows NT 10.0;Win64;x64) AppleWebKit/537.36(KHTML,likeGecko) Chrome/66.0.3359.139 Safari/537.36'
#         }
#
#     def single_proxy_handler(self,proxy):
#
#         try:
#             if isinstance(proxy,bytes):
#                 proxy = proxy.decode("utf-8")
#             real_proxy = {
#                 'http':'http://' + proxy,
#                 'https':'https://' + proxy,
#             }
#             print("正在测试",proxy)
#             result = requests.get(url=self.TEST_URL,proxies=real_proxy,headers=self.headers,timeout=1)
#             print("------")
#             print(result.status_code)
#             if result.status_code in self.VALID_STATUS_CODES:
#                 self.proxiespool.max(proxy)
#                 print("代理可用",proxy)
#             else:
#                 self.proxiespool.decrease(proxy)
#                 print("请求响应码不合法",proxy)
#         except Exception:
#             self.proxiespool.decrease(proxy)
#             print("代理请求失败", proxy)
#
#     def run(self):
#         # self.single_proxy_handler()
#         times = 0
#         spawms = []
#         proxy_list = self.proxiespool.all()
#         # print(proxy_list)
#         # print(proxy_list)
#         # proxy_list = [('122.114.31.177:808',)]
#         for proxy in proxy_list:
#             times += 1
#             proxy = proxy[0]
#             # print(proxy)
#             self.single_proxy_handler(proxy)
#             # print(proxy)
#             if times%5 == 0:
#                 time.sleep(5)
#             spawms.append(gevent.spawn(self.single_proxy_handler,proxy))
#         print(spawms)
#         gevent.joinall(spawms)
#
def main():
    p = Tester()
    p.run()
    # run()


if __name__ == '__main__':
    main()