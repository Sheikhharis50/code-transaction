from time import sleep

from transaction import Transaction, TransactionJob
from utils.logger import logger


def task(num: int, raise_exception: bool = False):
    logger.info(f"Task{num} is running.")
    sleep(2)
    if raise_exception:
        raise Exception(f"Task{num} failed to execute.")
    logger.info(f"Task{num} is executed.")


def callback(num: int):
    logger.info(f"Executing callback{num}.")
    sleep(2)
    logger.info(f"Callback{num} is executed.")


def main():
    with Transaction() as tran:
        tran.add_task(TransactionJob(job=task, args=(1,)))
        tran.add_callback(TransactionJob(job=callback, args=(1,)))
        tran.add_task(TransactionJob(job=task, args=(2,)))
        tran.add_callback(TransactionJob(job=callback, args=(2,)))
        tran.add_task(TransactionJob(job=task, args=(3, True)))
        tran.add_callback(TransactionJob(job=callback, args=(3,)))
        tran.add_task(TransactionJob(job=task, args=(4,)))
        tran.add_callback(TransactionJob(job=callback, args=(4,)))
    del tran


if __name__ == "__main__":
    main()
    exit(0)
