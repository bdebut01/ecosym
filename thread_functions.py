# Module taken from Mark Sheldon's COMP 50 class notes

import threading

def with_lock(lock, function):
    lock.acquire()
    try:
        value = function()
    finally:
        lock.release()

    return value

