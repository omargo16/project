from concurrent.futures import ThreadPoolExecutor
import logging


logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',)


def my_task(n):
    print(f"Processing {n}")


def main():
    logging.debug("Starting")
    with ThreadPoolExecutor(max_workers=3) as executor:
        my_task1 = executor.submit(my_task, 1)
        my_task2 = executor.submit(my_task, 2)
        my_task3 = executor.submit(my_task, 3)
    logging.debug("All tasks complete")


if __name__ == '__main__':
    main()
