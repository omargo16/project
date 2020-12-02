from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from multiprocessing import Process
import logging


class ThreadsExample:

    logging.basicConfig(
        level=logging.DEBUG,
        format='(%(threadName)-10s) %(message)s',)

    def daemon(self, a):
        logging.debug('Starting deamon')
        for i in range(10):
            print(i)
        logging.debug('Exiting')
        return f"hola {a}"

    def non_daemon(self):
        logging.debug('Starting')
        for i in range(100):
            print(i)
        logging.debug('Exiting')

    def start_ThreadNormal(self):
        thread1 = Thread(target=self.non_daemon)
        thread2 = Thread(
            target=self.daemon,
            args=("mundo",),
            daemon=True)
        thread2.start()
        thread1.start()

    def start_ThreadPool(self):
        with ThreadPoolExecutor() as executor:
            future = executor.submit(self.daemon, "mundo")
            executor.submit(self.non_daemon)
            return_value = future.result()
            print(return_value)

    def start_Process(self):
        process = Process(target=self.daemon, args=('Mundo',))
        process.start()


my_process = ThreadsExample()
# my_process.start_ThreadNormal()
my_process.start_ThreadPool()
# my_process.start_Process()

