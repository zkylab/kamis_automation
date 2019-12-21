# -*- coding: utf-8 -*-
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup
from requests import request
import ssl

# Common configs
requests.packages.urllib3.disable_warnings()

ctx = ssl.create_default_context()
# PURPOSE : get all links and images
all_own_links = []
all = {}

baseUrl = "https://www.turkiye.gov.tr"
# PURPOSE : get all links and images
def get_all_links(url):
    with urlopen(url) as response:
        html = response.read()
    bsObj = BeautifulSoup(html, 'lxml')
    links = [link.attrs['href'] if not link.attrs['href'].startswith("#") else None for link in bsObj.findAll('a')]
    all['link-text'] = [text.contents[0] for text in bsObj.findAll('a')]
    links = [link for link in links if link is not None]
    final_links = list(map(lambda link: baseUrl + '/' + link if not link.lower().startswith(("http", "https")) else link, links))
    own_links = list(map(lambda link: link if link.startswith(baseUrl) else None, final_links))
    # TODO: sometimes src is not enough to cover all images, modify it
    images = [link.get('src').replace("//", "http://") for link in bsObj.findAll('img')]
    all["images"] = images
    all['final_links'] = final_links
    will_be_recorded = list(set(map(lambda x: x if x not in all_own_links else None,own_links)))
    will_be_recorded = [x for x in will_be_recorded if x is not None]
    all_own_links.extend(will_be_recorded)
    if will_be_recorded:
        for own_link in will_be_recorded:
            get_all_links(own_link)
    return all



