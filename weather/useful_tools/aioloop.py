from concurrent.futures.thread import ThreadPoolExecutor
from tornado.concurrent import Future, chain_future

from tornado.ioloop import IOLoop
import multiprocessing


def execute_ioloop(func, *args):
    """ Ioloop Convert Function """
    pool = ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())
    old_future = pool.submit(func, *args)
    new_future = Future()
    IOLoop.current().add_future(old_future, lambda fut: chain_future(fut, new_future))
    return new_future
