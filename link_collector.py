# -*- coding: utf-8 -*-
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup

from requests import request

# Common configs
requests.packages.urllib3.disable_warnings()

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


# TEST, check images size
def check_image_size(images, image_size_max):
    exceed_images = {}
    for image_link in images:
        img = urlopen(image_link)
        if int(img.headers['content-length']) > image_size_max:
            exceed_images[image_link] = img.headers['content-length']
    return exceed_images


# TEST, check link length
def check_link_len(links, link_size_max):
    long_links = {}
    for link in links:
        if (len(link) > link_size_max):
            long_links[link] = len(link)
    return long_links


# TEST, check title length
def check_title_len(links, title_size_max, ):
    long_titles = {}
    for link in links:
        page = urlopen(link)
        page_soup = BeautifulSoup(page, "lxml")
        if page_soup.title is not None:
            if len(page_soup.title.string) > title_size_max:
                long_titles[link] = page_soup.title.string
    return long_titles


def check_response_time(links, response_time_max):
    exceed_response_time = {}
    for link in links:
        timeout = False
        try:
            response = requests.get(link, verify=False, timeout=5)
        except:
            elapsed_time = 9999
            timeout = True
        if timeout is False:
            elapsed_time = response.elapsed.total_seconds()
        if (elapsed_time > response_time_max):
            exceed_response_time[link] = elapsed_time
    return exceed_response_time


all = get_all_links(baseUrl)
exceed_images = check_image_size(all['images'], 4500)
exceed_response_time = check_response_time(all['images'], 1)

print(exceed_response_time)
