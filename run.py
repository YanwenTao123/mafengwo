import time
from multiprocessing import Pool
import os
from scrapy import cmdline
from freeTravel.data_analysis import DataViews
# commands内一起执行
# def run():
#     cmdline.execute("scrapy crawlall".split())

# 进程池
# def detailMsg_handler():
#     time.sleep(50)
#     cmdline.execute("scrapy crawl detailMsg".split())
# def freeTravel_handler():
#     cmdline.execute("scrapy crawl freeTravel".split())
# def run():
#     pool = Pool()
#     pool.apply_async(func=freeTravel_handler)
#     pool.apply_async(func=detailMsg_handler)
#     pool.close()
#     pool.join()

def run(task):
    # cmdline.execute(task)
    os.system(task)

if __name__ == "__main__":
    DataViews = DataViews()
    pool = Pool()
    tasks = ["scrapy crawl free_travel","scrapy crawl detailMsg"]
    for task in tasks:
        run(task)
    pool.apply_async(func=DataViews.hot_time)
    pool.apply_async(func=DataViews.hot_city)
    pool.apply_async(func=DataViews.attention_bar)
    pool.apply_async(func=DataViews.genderAnalysis)
    pool.close()
    pool.join()
