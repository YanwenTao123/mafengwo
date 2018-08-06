from multiprocessing import Process
from API_Module import app
from checkModule import Tester
from getModule import GetProxy
import time

class Schedurer():
    def __init__(self):
        self.TEST_CYCLE = 20
        self.GET_CYCLE = 5
        self.TEST_ENABLED = 1
        self.GET_ENABLED = 1
        self.API_ENBLED = 1

    def shed_test(self):
        tester = Tester()
        while 1:
            tester.run()
            time.sleep(self.TEST_CYCLE)

    def shed_get(self):
        getter = GetProxy()
        while 1:
            getter.run()
            time.sleep(self.GET_CYCLE)

    def shed_api(self):
        while 1:
            app.run(
                host='127.0.0.1',
                port=7777,
                debug=True)

    def run(self):
        api_process = Process(target=self.shed_api)
        tester_process = Process(target=self.shed_test)
        get_process = Process(target=self.shed_get)
        get_process.start()
        api_process.start()
        tester_process.start()

def main():
    p = Schedurer()
    p.run()

if __name__ == "__main__":
    main()

