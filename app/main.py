from time import sleep

from transaction import Transaction
from utils.logger import logger


def task(num: int, raise_exception: bool = False):
    logger.info(f"Task{num} is running.")
    sleep(2)
    if raise_exception:
        raise Exception(f"Task{num} failed to execute.")
    logger.info(f"Task{num} is executed.")


def callback(num: int):
    logger.info(f"Executing task{num} rollback.")
    sleep(2)
    logger.info(f"Task{num} rollback is executed.")


def main():
    with Transaction() as tran:
        tran.add_task(task, 1)
        tran.add_callback(callback, 1)
        tran.add_task(task, 2)
        tran.add_callback(callback, 2)
        tran.add_task(task, 3, True)
        tran.add_callback(callback, 3)
        tran.add_task(task, 4)
        tran.add_callback(callback, 4)
    del tran


if __name__ == "__main__":
    main()
    exit(0)
