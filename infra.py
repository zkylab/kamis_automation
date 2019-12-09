# -*- coding: utf-8 -*-
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup
from requests import request
import ssl

# Common configs
requests.packages.urllib3.disable_warnings()

all_own_links = []

ctx = ssl.create_default_context()
# PURPOSE : get all links and images
def get_all_links(url):
    all = {}
    with urlopen(url, context= ctx, timeout=4) as response:
        html = response.read()
    bsObj = BeautifulSoup(html, 'lxml')
    links = [link.attrs['href'] if not link.attrs['href'].startswith("#") else None for link in bsObj.findAll('a')]
    links = [link for link in links if link is not None]
    final_links = list(map(lambda link: url + link if not link.lower().startswith(("http", "https")) else link, links))
    # own_links = list(map(lambda link: link if link.startswith(url)
    # else None, final_links))
    # TODO: sometimes src is not enough to cover all images, modify it
    images = [link.get('src').replace("//", "http://") for link in bsObj.findAll('img')]
    all["images"] = images
    all['final_links'] = final_links
    # all_own_links.extend(own_links)
    # for own_link in own_links:
    #     get_all_links(own_link)
    return all


