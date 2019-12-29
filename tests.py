from urllib.request import urlopen

import requests
from string import printable


# TEST, check images size
def check_image_size(images, image_size_max):
    exceed_images = {}
    for image_link in images:
        try:
            img = urlopen(image_link)
        except:
            continue
        if int(img.headers['content-length']) > image_size_max:
            exceed_images[image_link] = img.headers['content-length']
    return exceed_images


# TEST, check link length
def check_link_len(links, link_size_max):
    long_links = {}
    for link in links:
        if len(link) > link_size_max:
            long_links[link] = len(link)
    return long_links


# TEST, check title length
def check_title_len(titles, title_size_max, ):
    long_titles = {}
    for title in titles.values():
        if len(title) > title_size_max:
            long_titles[title] = len(title)
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
        if elapsed_time > response_time_max:
            exceed_response_time[link] = elapsed_time
    return exceed_response_time


def check_link_text_length(link_texts, max_length):
    exceed_link_texts = {}
    for link_text in link_texts.values():
        if len(link_text) > max_length:
            exceed_link_texts[link_text] = len(link_text)
    return exceed_link_texts


def check_special_character(link_texts):
    special_character_texts = []
    for link_text in link_texts.values():
        if set(link_texts).difference(printable):
            special_character_texts.append(link_text)
    return special_character_texts
