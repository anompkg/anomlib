import hashlib, os, sys
from pathlib import Path

import anomlib.pillow

home = Path.home()

anomtoolDoCache = home / ".cache/anomtool/do"
anomtoolDoHistory = anomtoolDoCache / "history"
anomtoolDoLog = anomtoolDoCache / "do.log"


anomlib.pillow.mkdirs(str(anomtoolDoCache))
anomlib.pillow.mkdirs(str(anomtoolDoHistory))



def num_to_index(start, stop, end, url_begin="", urlend=""):
    fixture = len(str(end)) - len(str(start))
    # Fix url_begin if the number's power is weak
    url_begin = '0' * fixture
    return f'{url_begin}{start}'
    request = f'{url_begin}[{start}-{stop}]{urlend}'


def get_range(numbers, fixture):
    fixture -= len(str(numbers[0])) - 1
    patch = '0' * fixture
    start = numbers[0]
    stop = numbers[-1]
    return startpatch+start, patch+stop

def get_ranges(start, stop):
    stop += 1
    fixture = len(str(stop)) - len(str(start))
    result = []
    powers = {}
    for i in [str(i) for i in range(start, stop)]:
        if str(len(i)) not in powers:
            powers[str(len(i))] = []
        powers[str(len(i))] += [i]
    print(powers)
    for power, numbers in powers.items():
        result += [get_range(numbers, fixture)]
    return result
        

print(get_ranges(1, 8000))
print(get_ranges(1, 900))
print(get_ranges(1, 90))
print(get_ranges(1, 9))

