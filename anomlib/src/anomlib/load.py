"""Library for testing similar/compatible functions on speed.
We prioritize speed and space usage.
Speed tests should be categorized and stored for future work.
"""

import time
from functools import reduce
from operator import itemgetter

import numpy as np

np.set_printoptions(suppress=True, precision=30)  # For standard form


def sortby(d, field='name', key=None, reverse=False):
    if not key:
        key = itemgetter(field)
    return sorted(d, key=key, reverse=reverse)


def add(*args):
    "Sum numbers and return as numpy"
    return np.array(sum(*args))


def sum_fields(d, field='name'):
    "Sum each field in listed dicts"
    return reduce(lambda x, y: {field: add(x[field], y[field])}, d)[field]


def speed_test(fn, *cases) -> list:
    """Rank all similar functions by Speed"""

    results = []

    for params in cases:
        # Get arguments
        args = params['args']
        kwargs = params['kwargs']

        "Test function on time for specific case"

        # Prepare space for the results
        name = fn.__name__
        status = {}

        # Measure execution time
        started = time.time()
        print('args and kwargs: ', args, kwargs)
        result = fn(*args, **kwargs)
        ended = time.time()

        # Categorize results
        status["name"] = name
        status["result"] = result
        status["speed"] = np.array(ended - started)
        results += [status]

    # Sort time by speed
    results = sortby(results, 'speed')
    print('sorted results: ', results)

    return results


def data_usage_test(fn, *cases):
    """Rank all similar functions by Data Usage"""


def speed_tests(fns: list, *cases):
    """Rank all similar functions by Speed in all cases"""
    results = {}
    for fn in fns:
        # Prepare space for the results
        name = fn.__name__
        if name not in results:
            results[name] = {}
            results[name]['speed'] = 0

        # Get speed count
        speed = results[name]['speed']

        result = speed_test(fn, *cases)

        # Update speed summary
        speed += sum_fields(result, 'speed')

        # Convert sum back to readable format
        results[name]['speed'] = np.array(speed)

    return results


def data_usage_tests(fns: list, *cases) -> dict:
    """Rank all similar functions by Data Usage in all cases"""
    for fn in fns:
        data_usage_test(fn, *cases)
