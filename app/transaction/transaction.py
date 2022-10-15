from dataclasses import dataclass, field
from queue import LifoQueue, SimpleQueue
from typing import Any, Callable, Dict, Tuple

from utils.logger import logger

from .exceptions import CallableError, NotEnoughError


@dataclass
class TransactionJob:
    job: Callable[..., None]
    args: Tuple[Any] = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    ignore_failed: bool = False

    def __post_init__(self):
        self.validate()

    def validate(self):
        if not callable(self.job):
            raise CallableError(str(self.job))


class Transaction:
    def __init__(self) -> None:
        self._tasks = SimpleQueue()
        self._callbacks = LifoQueue()

    def add_task(self, task: TransactionJob):
        if self._tasks.qsize() != self._callbacks.qsize():
            raise NotEnoughError("callbacks")

        self._tasks.put(task)

    def add_callback(self, callback: TransactionJob):
        if self._tasks.qsize() == self._callbacks.qsize():
            raise NotEnoughError("tasks")

        self._callbacks.put(callback)

    def _execute(self):
        """
        Execute all the tasks in queue.
        """
        while not self._tasks.empty():
            task: TransactionJob = self._tasks.get()
            try:
                task.job(*task.args, **task.kwargs)
            except Exception as e:
                logger.error(e)
                if not task.ignore_failed:
                    self._rollback()
                    break
                logger.info("Ignoring....")

            self._callbacks.get() if not self._callbacks.empty() else None

    def _rollback(self):
        """
        Rollback if any exception is occurred.
        """
        while not self._callbacks.empty():
            callback: TransactionJob = self._callbacks.get()
            try:
                callback.job(*callback.args, **callback.kwargs)
            except Exception as e:
                logger.error(e)
                if not callback.ignore_failed:
                    break
                logger.info("Ignoring....")

    def __enter__(self) -> "Transaction":
        return self

    def __exit__(self, *args, **kwargs):
        self._execute()

        del self._tasks
        del self._callbacks
