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


def getGallery(start, stop, url_begin="file_", urlend=".jpg",
               ggHome=ggHome, ggType=ggType):
    hash = anomlib.pillow.hashedString(url_begin + urlend)
    print(hash)
    requests = curlRange(start, stop, url_begin, urlend)
    
    ggDir = Path(ggHome) / hash
    
    # Do not proceed if dir alr exist
    if os.path.isdir(ggDir):
        print(f"The {hash} Files are already downloaded")
        return
    
    # Fixme: Check that dir does not exist and then proceed
    anomlib.pillow.mkdirs(str(ggDir))
    
    # Fixme: Change directory to current working directory
    os.chdir(ggDir)

    print(requests)
    for request in requests:
        print(f"curl '{request}' -o 'local2-#1.{ggType}'")
        anomlib.shell.runcmd(f"curl {request} -o 'local-#1.{ggType}'")



# print()
# # print(getGallery(1, 900, "file", ".png"))
# # print(getGallery(1, 90, "file-", ".jpeg"))
# print(getGallery(1, 23, "https://image.hdporncomics.com/uploads/disguised-lust-0", ".jpg"))
# # print(getGallery(1, 5, "https://image.hdporncomics.com/uploads/angel-x-stitch-00", ".jpg"))
# # print(getGallery(1, 11, "https://im.hdporncomics.com/uploads/560facf644dc7837b5bd6f2a726c6582/she-s-not-little-anymore-0", ".jpg"))

