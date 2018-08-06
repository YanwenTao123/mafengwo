# from storageModule import RedisClient
#
# class get_proxies():
#     def __init__(self):
#         self.redis = RedisClient()
#
#     def get_proxy(self):
#         return self.redis.random().decode('utf-8')

from flask import Flask,g
from storage import MysqlClient

app = Flask(__name__)
def get_conn():
    if not hasattr(g,'proxiespool'):
        g.mysql = MysqlClient()
    return g.mysql

@app.route('/')
def index():
    return '<h2>welcome to proxy pool system</h2>'

@app.route('/random')
def get_proxy():
    conn = get_conn()
    return conn.random()

@app.route('/count')
def count():
    conn = get_conn()
    return str(conn.count())

if __name__ == "__main__":
    app.run(
        host='127.0.0.1',
        port=7777,
        debug=True
    )

