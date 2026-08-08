"""Library for testing similar/compatible functions on speed.
We prioritize speed and space usage.
Speed tests should be categorized and stored for future work.
"""

import time
from functools import reduce
from operator import itemgetter


def sortby(d, field='name', key=None, reverse=False):
    if not key:
        key=itemgetter(field)
    return sorted(d, key=key, reverse=reverse)

def sum_fields(d, field='name'):
    "Sum each field in listed dicts"
    return reduce(lambda x, y: {field: x[field] + y[field]}, d)[field]

def speed_test(fns: list, *args, **kwargs) -> dict:
    """Rank all similar functions by Speed"""

    results = []

    for fn in fns:
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
        status["speed"] = ended - started
        results += [status]

    # Sort time by speed
    results = sortby(results, 'speed')
    print(results)

    return results

def data_usage_test(fns: list, *args, **kwargs) -> dict:
    """Rank all similar functions by Data Usage"""
    for fn in fns:
        fn(*args, **kwargs)

def speed_tests(fns: list, *cases):
    """Rank all similar functions by Speed in all cases"""
    print(cases)
    for params in cases:
        print(params)
        args = params['args']
        kwargs = params['kwargs']
        results = speed_test(fns, *args, **kwargs)
        return sum_fields(results, 'speed')

def data_usage_tests(fns: list, *cases) -> dict:
    """Rank all similar functions by Data Usage in all cases"""
    for params in cases:
        print(params)
        args = params['args'], kwargs = params['kwargs']
        data_usage_test(fns, *args, **kwargs)


