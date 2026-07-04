""" Y2 is a Youtube parser for fun.
I will try to call invidious and/or youtube and play with their stuff they give me.
The more info we reach the more stuff we can do with it.
"""

import requests
from bs4 import BeautifulSoup

# Fetch the page directly
url = "https://www.youtube.com/playlist?list=PLRBp0Fe2Gpgn8Y9qI-p0aTxVtw8onBSFj"
html = requests.get(url).text

# Parse the HTML with BeautifulSoup + lxml
soup = BeautifulSoup(html, "lxml")

# Extract the title and all links
print(soup.title.get_text())

for link in soup.select("a[href]"):
    print(link["href"])


# We will try different stratagies such us using different sites.
# We will cache requests over to minimise the calls to google.

