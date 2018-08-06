import os
import pymongo
import matplotlib
from matplotlib import pyplot as plt
import numpy as np

class DataViews():
    def __init__(self):
        self.client = pymongo.MongoClient(host="localhost",port=27017)
        self.db = self.client['mafengwo']
        self.collection = self.db["mafengwo"]
        self.collection_detail = self.db['detailMsg']
        matplotlib.rcParams['font.sans-serif'] = 'SimHei'
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']
        matplotlib.rcParams['axes.unicode_minus'] = False

    def all_np(self,arr):
        """目的地城市数目分析"""
        arr = np.array(arr)
        key = np.unique(arr)
        result = {}
        for k in key:
            mask = (arr == k)
            arr_new = arr[mask]
            v = arr_new.size
            result[k] = v
        return result

    def genderAnalysis(self):
        """发起人性别比例"""
        female = self.collection.find({"gender":"1"}).count()
        male = self.collection.find({"gender":"0"}).count()
        all = self.collection.find().count()
        # plt.figure(figsize=(6,9))
        plt.title("热门自由行发起人男女比例")
        labels = ["famale","male"]
        sizes = [(female/all)*100,(male/all)*100]
        colors = ["red","yellow"]
        explode = (0.1,0)
        plt.pie(sizes,explode=explode,colors=colors,labeldistance=1.1,labels=labels,autopct="%3.1f%%",pctdistance=0.6,startangle=90,shadow=0.5)
        plt.axis('equal')
        plt.legend()
        if not os.path.exists(r"G:\scrapy_execise\freeTravel\freeTravel\img\gender_pie.jpg"):
            plt.savefig(r"G:\scrapy_execise\freeTravel\freeTravel\img\gender_pie.jpg")
        else:
            os.remove(r"G:\scrapy_execise\freeTravel\freeTravel\img\gender_pie.jpg")
            plt.savefig(r"G:\scrapy_execise\freeTravel\freeTravel\img\gender_pie.jpg")
        plt.show()

    def attention_bar(self):
        """最受关注自由行的发起人"""
        top_10 = []
        left = []
        height = []
        l = self.collection.find({},{"_id":0,"initiator":1,"attention":1}).sort('attention',-1).limit(50)
        for i in l:
            top_10.append(i)
        for i in top_10:
            # if len(i['city']) > 8:
            #     i['city'] = i['city'][0:8]+'...'
            left.append(i["initiator"])
            height.append(i["attention"])
            if len(set(left)) == 10:
                break
        plt.figure(figsize=(14,6))
        plt.barh(left,height)
        plt.title("自由行关注度top10")
        plt.xlabel("关注度")
        plt.ylabel("自由行发起人")
        if not os.path.exists(r"G:\scrapy_execise\freeTravel\freeTravel\img\attention_top10_bar.jpg"):
            plt.savefig(r"G:\scrapy_execise\freeTravel\freeTravel\img\attention_bar.jpg")
        else:
            os.remove(r"G:\scrapy_execise\freeTravel\freeTravel\img\attention_bar.jpg")
            plt.savefig(r"G:\scrapy_execise\freeTravel\freeTravel\img\attention_bar.jpg")
        plt.show()

    def hot_city(self):
        """最受关注的自由行热门城市"""
        all_city_mongo = self.collection.find({},{"_id":0,"city":1})
        al_city = []
        left = []
        height = []
        for i in all_city_mongo:
            al_city.append(i["city"])
        dct = self.all_np(al_city)
        city_top10 = sorted(dct.items(),key = lambda dct:dct[1],reverse=True)[0:10]
        # print(city_top10)
        for i in city_top10:
            left.append(i[0])
            height.append(i[1])
        plt.bar(left,height)
        plt.title("自由行热门地点top10")
        for a, b in zip(left,height):
            # 写上数据标签，a,b表示写文本的位置，%f写文本的内容，ha水平对齐方式，va垂直对齐方式
            plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=7)
        if not os.path.exists(r"G:\scrapy_execise\freeTravel\freeTravel\img\hot_destination_top10_bar.jpg"):
            plt.savefig(r"G:\scrapy_execise\freeTravel\freeTravel\img\hot_destination_bar.jpg")
        else:
            os.remove(r"G:\scrapy_execise\freeTravel\freeTravel\img\hot_destination.jpg")
            plt.savefig(r"G:\scrapy_execise\freeTravel\freeTravel\img\hot_destination.jpg")
        plt.show()

    def hot_time(self):
        Early_Aug = self.collection_detail.find({"departure_time":{"$lte":'2018-08-15'}}).count()
        Late_Aug = self.collection_detail.find({"$and":[{"departure_time":{"$gt":'2018-08-15'}},{"departure_time":{"$lte":'2018-08-31'}}]}).count()
        Early_Sup = self.collection_detail.find({"$and":[{"departure_time":{"$gte":'2018-09-01'}},{"departure_time":{"$lte":'2018-09-15'}}]}).count()
        Late_Sup = self.collection_detail.find(
            {"$and": [{"departure_time": {"$gt": '2018-09-15'}}, {"departure_time": {"$lte": '2018-09-30'}}]}).count()
        Early_Oct = self.collection_detail.find(
            {"$and": [{"departure_time": {"$gte": '2018-10-01'}}, {"departure_time": {"$lte": '2018-10-15'}}]}).count()
        Late_Oct = self.collection_detail.find(
            {"$and": [{"departure_time": {"$gt": '2018-10-15'}}, {"departure_time": {"$lte": '2018-10-31'}}]}).count()
        Early_Nov = self.collection_detail.find(
            {"$and": [{"departure_time": {"$gte": '2018-11-01'}}, {"departure_time": {"$lte": '2018-11-15'}}]}).count()
        Late_Nov = self.collection_detail.find(
            {"$and": [{"departure_time": {"$gt": '2018-11-15'}}, {"departure_time": {"$lte": '2018-11-30'}}]}).count()
        Early_Dec = self.collection_detail.find(
            {"$and": [{"departure_time": {"$gte": '2018-12-01'}}, {"departure_time": {"$lte": '2018-12-15'}}]}).count()
        Late_Dec = self.collection_detail.find(
            {"$and": [{"departure_time": {"$gt": '2018-12-15'}}, {"departure_time": {"$lte": '2018-12-31'}}]}).count()
        Next_year = self.collection_detail.find({"departure_time":{"$gte":'2019-01-01'}}).count()
        left = ["Early_Aug","Late_Aug","Early_Sup","Late_Sup","Early_Oct","Late_Oct","Early_Nov","Late_Nov","Early_Dec","Late_Dec","Next_year"]
        height = [Early_Aug,Late_Aug,Early_Sup,Late_Sup,Early_Oct,Late_Oct,Early_Nov,Late_Nov,Early_Dec,Late_Dec,Next_year]
        plt.figure(figsize=(10,6))
        plt.title("各时间段自由行热度")
        for a,b in zip(left,height):
            plt.text(a,b+0.05,"%.0f" % b,va="bottom",ha="center",fontsize=12)
        plt.plot(left,height)
        plt.xlabel("Month")
        plt.ylabel("各时间段出行次数")
        if not os.path.exists(r"G:\scrapy_execise\freeTravel\freeTravel\img\hot_time_plot.jpg"):
            plt.savefig(r"G:\scrapy_execise\freeTravel\freeTravel\img\hot_time_plot.jpg")
        else:
            os.remove(r"G:\scrapy_execise\freeTravel\freeTravel\img\hot_time_plot.jpg")
            plt.savefig(r"G:\scrapy_execise\freeTravel\freeTravel\img\hot_time_plot.jpg")
        plt.show()
        # print(Early_August,Late_August,Early_Sup,Late_Sup,Early_Oct,Late_Oct,Early_Nov,Late_Nov,Early_Dec,Late_Dec,Next_year)





if __name__ == "__main__":
    p = DataViews()
    p.hot_time()