
home = Path.home()

anomtoolDoCache = home / ".cache/anomtool/do"
anomtoolDoHistory = anomtoolDoCache / "history"
anomtoolDoLog = anomtoolDoCache / "do.log"


pillow.mkdirs(str(anomtoolDoCache))
pillow.mkdirs(str(anomtoolDoHistory))



def num_to_index(start, stop, end, url_begin="", urlend=""):
    fixure = len(str(end)) - len(str(start))
    # Fix url_begin if the number's power is weak
    url_begin = '0' * fixure
    return f'{url_begin}{start}'
    request = f'{url_begin}[{start}-{stop}]{urlend}'


def get_range(numbers):
    start = numbers[0]
    stop = numbers[-1]
    return start, stop

def get_ranges(start, stop):
    powers = {}
    for i in [str(i) for i in range(start, stop+1)]:
        if str(len(i)) not in powers:
            powers[str(len(i))] = []
        powers[str(len(i))] += [i]
    print(powers)
    for power, numbers in powers.items():
        print(get_range(numbers))
        

get_ranges(1, 90, 9000)
get_ranges(1, 9000, 9000)
