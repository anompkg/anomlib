# test_my_urllib.py
import pytest

from anomlib.url_range import changed_numbers


def test_changed_numbers_ignores_leading_zeros():
    url1 = "https://site.com/images/item-00001.png?size=large"
    url2 = "https://cdn.example.org/images/item-00156.png?size=large"

    assert changed_numbers(url1, url2) == (1, 156)


def test_changed_numbers_raises_when_no_changed_number():
    url1 = "https://site.com/image.png"
    url2 = "https://cdn.example.org/image.png"

    with pytest.raises(ValueError, match="changed number"):
        changed_numbers(url1, url2)
