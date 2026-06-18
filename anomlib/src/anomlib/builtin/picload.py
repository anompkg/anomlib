import hashlib, os, sys
from pathlib import Path

import anomlib.pillow

home = Path.home()

ggHome = home / "Pictures/gg"
ggType = "jpeg"
anomlib.pillow.mkdirs(str(ggHome))



def num_to_index(start, stop, end, url_begin="", urlend=""):
    fixture = len(str(end)) - len(str(start))
    # Fix url_begin if the number's power is weak
    url_begin += '0' * fixture
    request = f'{url_begin}[{start}-{stop}]{urlend}'
    return request


def get_range(numbers, fixture):
    fixture -= len(str(numbers[0])) - 1
    patch = '0' * fixture
    start = numbers[0]
    stop = numbers[-1]
    return start, stop

def get_ranges(start, stop):
    stop += 1
    fixture = len(str(stop)) - len(str(start))
    result = []
    powers = {}
    for i in [str(i) for i in range(start, stop)]:
        if str(len(i)) not in powers:
            powers[str(len(i))] = []
        powers[str(len(i))] += [i]
    for power, numbers in powers.items():
        result += [get_range(numbers, fixture)]
    return result
        
def curlRange(start, stop, url_begin="file_", urlend=".jpg"):
    result = []
    # stop += 1
    for a, b in get_ranges(start, stop):
        print ("a,b:", a, b)
        result += [num_to_index(a, b, stop, url_begin, urlend)]
    return result


def getGallery(start, stop, url_begin="file_", urlend=".jpg"):
    hash = anomlib.pillow.hashedString(url_begin + urlend)
    print(hash)
    requests = curlRange(start, stop, url_begin, urlend)
    
    # Fixme: Do not proceed if dir alr exist
    
    # Fixme: Check that dir does not exist and then proceed
    
    # Fixme: Change directory to current working directory
    
    anomlib.pillow.mkdirs(str(ggHome / hash))
    
    print(requests)
    # for request in requests:
    #     anomlib.shell.runcmd(f"curl {request} -o 'local-#1.{ggType}'")



print()
print(getGallery(1, 900, "file", ".png"))
print(getGallery(1, 90, "file-", ".jpeg"))
print(getGallery(1, 9, "file0", ".jpg"))

