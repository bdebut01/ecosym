import threading
import random

def with_lock(lock, function):
    """ Function taken from Mark Sheldon's COMP 50 class notes """
    lock.acquire()
    try:
        value = function()
    finally:
        lock.release()

    return value


def random_pick(some_list, probabilities):
    """ Function written by Kevin Park and Peter Cogolo, as seen in Python
        Cookbook, 2nd Editions: http://bit.ly/1QfSwDs
    """
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    for item, item_probability in zip(some_list, probabilities):
        cumulative_probability += item_probability
        if x < cumulative_probability: break
    return item

