from time import sleep

from transaction import Transaction, TransactionJob
from utils.logger import logger


def task(num: int, raise_exception: bool = False):
    """
    It sleeps for 2 seconds and then logs a message

    :param num: The number of the task
    :type num: int
    :param raise_exception: If True, the task will raise an exception, defaults to False
    :type raise_exception: bool (optional)
    """
    logger.info(f"Task{num} is running.")
    sleep(2)
    if raise_exception:
        raise Exception(f"Task{num} failed to execute.")
    logger.info(f"Task{num} is executed.")


def callback(num: int):
    """
    It sleeps for 2 seconds and logs the fact that it's doing so

    :param num: int - the number of the callback
    :type num: int
    """
    logger.info(f"Executing callback{num}.")
    sleep(2)
    logger.info(f"Callback{num} is executed.")


def main():
    with Transaction() as tran:
        tran.add_task(TransactionJob(job=task, args=(1,)))
        tran.add_callback(TransactionJob(job=callback, args=(1,)))
        tran.add_task(TransactionJob(job=task, args=(2,)))
        tran.add_callback(TransactionJob(job=callback, args=(2,)))
        tran.add_task(TransactionJob(job=task, args=(3, True), ignore_failed=True))
        tran.add_callback(TransactionJob(job=callback, args=(3,)))
        tran.add_task(TransactionJob(job=task, args=(4, True)))
        tran.add_callback(TransactionJob(job=callback, args=(4,)))
        tran.add_task(TransactionJob(job=task, args=(5,)))
        tran.add_callback(TransactionJob(job=callback, args=(5,)))
    del tran


if __name__ == "__main__":
    main()
    exit(0)
