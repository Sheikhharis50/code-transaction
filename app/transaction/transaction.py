from queue import LifoQueue, SimpleQueue
from typing import Callable

from utils.logger import logger

from .exceptions import CallableError, NotEnoughError


class Transaction:
    def __init__(self) -> None:
        self._tasks = SimpleQueue()
        self._callbacks = LifoQueue()

    def add_task(self, task: Callable, *args, **kwargs):
        if not callable(task):
            raise CallableError(str(task))

        if self._tasks.qsize() != self._callbacks.qsize():
            raise NotEnoughError("callbacks")

        self._tasks.put((task, args, kwargs))

    def add_callback(self, callback: Callable, *args, **kwargs):
        if not callable(callback):
            raise CallableError(str(callback))

        if self._tasks.qsize() == self._callbacks.qsize():
            raise NotEnoughError("tasks")

        self._callbacks.put((callback, args, kwargs))

    def _execute(self):
        """
        Execute all the tasks in queue.
        """
        while not self._tasks.empty():
            try:
                task, args, kwargs = self._tasks.get()
                task(*args, **kwargs)
                self._callbacks.get()
            except Exception as e:
                logger.error(e)
                self._rollback()
                break

    def _rollback(self):
        """
        Rollback if any exception is occurred.
        """
        while not self._callbacks.empty():
            try:
                callback, args, kwargs = self._callbacks.get()
                callback(*args, **kwargs)
            except Exception as e:
                logger.error(e)

    def __enter__(self) -> "Transaction":
        return self

    def __exit__(self, *args, **kwargs):
        self._execute()

        del self._tasks
        del self._callbacks
