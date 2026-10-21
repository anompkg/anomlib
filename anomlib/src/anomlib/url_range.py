from difflib import SequenceMatcher

import anomlib.compare

import re

url1 = "https://example.com/00001.png"
url2 = "https://example.com/00156.png"

# Concentrate only on changed parts in URLs
# Note we redefine urls, by omitting unchanged parts
urls = anomlib.compare.check_urlrange(url1, url2)
url1 = urls[0]
url2 = urls[1]


def number_from_url(url):
    """Check numbers inside url.
    Works only with urls that end on .png"""
    match = re.search(r"(\d+)\.png$", url)
    if not match:
        raise ValueError(f"No numbered PNG filename in {url!r}")
    return int(match.group(1))  # int() ignores leading zeros


numbers = number_from_url(url1), number_from_url(url2)
print(numbers)  # (1, 156)



def changed_numbers(url1: str, url2: str) -> tuple[int, int]:
    """Walk diff and merge changed and then return combined number.
    Note: this code was AI-generated and soon will be replaced with normal one.
    Code does its part but it does it the weird way bringing potential bug."""
    matcher = SequenceMatcher(None, url1, url2)

    print(url1)
    print(url2)
    print(matcher.get_matching_blocks())

    changed1 = []
    changed2 = []

    # Walk diff chunks and merge only changed into "changed"
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        print(i1, i2, j1, j2, tag)
        if tag != "equal":
            changed1.append(url1[i1:i2])
            changed2.append(url2[j1:j2])

    digits1 = "".join(ch for ch in "".join(changed1) if ch.isdigit())
    digits2 = "".join(ch for ch in "".join(changed2) if ch.isdigit())

    if not digits1 or not digits2:
        raise ValueError("Could not find a changed number in both URLs")

    return int(digits1), int(digits2)  # leading zeros are ignored


def curl_range_urls(template: str, start: int, end: int, width: int = 5) -> list[str]:
    """Build curl brace-range URLs, preserving zero-padding."""
    if start < 0 or end < start:
        raise ValueError("Expected 0 <= start <= end")

    urls = []
    first = start

    while first <= end:
        digits = len(str(first))
        last = min(end, 10**digits - 1)

        # Keep each range at a fixed filename width.
        prefix_zeros = "0" * max(0, width - digits)
        urls.append(
            template.replace("{number}", f"{prefix_zeros}{{{first}..{last}}}")
        )
        first = last + 1

    return urls


url1 = "https://site.com/images/item-00001.png?size=large"
url2 = "https://site.com/images/item-00156.png?size=large"

print(changed_numbers(url1, url2))  # (1, 156)

template = "https://site.com/images/item-{number}.png?size=large"
for url in curl_range_urls(template, 1, 156):
    print(url)
