from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup


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
            response = requests.get(link, verify=False, timeout=response_time_max)
        except:
            elapsed_time = 99999999
            timeout = True
        if timeout is False:
            elapsed_time = response.elapsed.total_seconds()
        if (elapsed_time > response_time_max):
            exceed_response_time[link] = elapsed_time
    return exceed_response_time
