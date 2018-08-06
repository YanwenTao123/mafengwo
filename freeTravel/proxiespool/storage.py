import pymysql
from random import choice

class MysqlClient():
    def __init__(self):
        """连接MYSQL"""
        self.max_score = 100
        self.min_score = 0
        self.initial_socre = 10
        self.HOST = 'localhost'
        self.PORT = 3306
        self.PASSWORD = "123456"
        self.db = 'proxies'
        self.user = "root"
        self.conn = pymysql.connect(host=self.HOST,port=self.PORT,password=self.PASSWORD,db =self.db,user=self.user)
        self.cursor = self.conn.cursor()

    def add(self,proxy):
        """添加代理到mysql,并设置初始值"""
        sql_insert = "INSERT INTO proxies(proxy,score) VALUES('{}','{}')".format(proxy,self.initial_socre)
        self.cursor.execute(sql_insert)
        self.conn.commit()

    def random(self):
        """随机返回一个代理，有最大的分值则优先"""
        sql_select_1 = "SELECT score FROM proxies ORDER BY score DESC"
        self.cursor.execute(sql_select_1)
        result_1 = self.cursor.fetchone()
        # print(result_1)
        sql_select_2 = 'SELECT proxy FROM proxies WHERE score = "{}"'.format(result_1[0])
        self.cursor.execute(sql_select_2)
        result_2 = self.cursor.fetchall()
        print(choice(result_2)[0])
        return choice(result_2)[0]

    def decrease(self,proxy):
        """代理连接失败，分值减一，到0移除出数据库"""
        sql_select = 'SELECT score FROM proxies WHERE proxy = "{}"'.format(proxy)
        self.cursor.execute(sql_select)
        score = self.cursor.fetchone()[0]
        # print(score)
        if score and score > self.min_score:
            print('代理',proxy,"当前分数",score,'减1')
            sql_update = 'UPDATE proxies SET score = score-1 WHERE proxy = "{}"'.format(proxy)
            self.cursor.execute(sql_update)
            self.conn.commit()
        else:
            print('代理',proxy,"当前分数",score,'移除')
            sql_delete = 'DELETE FROM proxies WHERE proxy = "{}"'.format(proxy)
            self.cursor.execute(sql_delete)
            self.conn.commit()

    def exists(self,proxy):
        """判断代理是否存在"""
        sql_select = 'SELECT score FROM proxies WHERE proxy = "{}"'.format(proxy)
        self.cursor.execute(sql_select)
        score = self.cursor.fetchone()
        return score == None

    def max(self,proxy):
        """设置为最大的分值"""
        print('代理', proxy, "可用，设置为", self.max_score)
        sql_update = 'UPDATE proxies SET score = 100 WHERE proxy = "{}"'.format(proxy)
        self.cursor.execute(sql_update)
        self.conn.commit()

    def count(self):
        """返回数据库的代理数量"""
        sql_select = 'SELECT score FROM proxies'
        rows = self.cursor.execute(sql_select)
        # print(rows)
        return rows

    def all(self):
        """返回全部的代理列表"""
        sql_select = 'SELECT proxy FROM proxies'
        self.cursor.execute(sql_select)
        result = self.cursor.fetchall()
        # print(result)
        return result

def main():
    p = MysqlClient()
    p.count()

if __name__ == "__main__":
    main()