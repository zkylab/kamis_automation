# -*- coding: utf-8 -*-
from requests_html import HTMLSession
import re

recursively_data = {"link-title": {}, "all-links": [], "images": [], "own-links": [], "link-texts": {}}
# this line should be taken from config (yaml etc.)

baseUrl ="http://isar.com.tr/"
# regex pattern for tel, mailto etc which are not actually links
mail_tel_regex = r"tel\:\d{1,}"
pattern = re.compile(mail_tel_regex)
link_text = {}


# Own Link length is hardly configured to provide testing purposes, since scrapping all pages is time consuming.
def recursive_link_collector(url):
    if len(recursively_data['own-links']) > 60:
        return 1
    session = HTMLSession()
    web_manager = session.get(url)
    all_links = set([linkz for linkz in web_manager.html.absolute_links if
                     linkz not in recursively_data['all-links'] and linkz.startswith(
                         ("https", "http"))])
    own_links = set([link for link in all_links if
                     link.startswith(baseUrl) and link is not baseUrl and not link in recursively_data['own-links']])

    link_texts = {}
    for linkz in web_manager.html.find('a'):
        link_text = linkz.full_text
        if len(link_text) > 1:
            link_texts[linkz.base_url] = link_text

    images = []
    for image in web_manager.html.find('img'):
        if not image.attrs['src'].startswith(("http", "https")):
            images_parsed = image.attrs['src']
            images.append(baseUrl + "/" + images_parsed)
        else:
            images_parsed = image.attrs['src']
            images.append(images_parsed)
    images_unique = set(images)

    link_title = {url: web_manager.html.find('title')[0].full_text}

    recursively_data['link-texts'].update(link_texts)
    recursively_data['link-title'].update(link_title)
    recursively_data['images'].extend(images_unique)
    recursively_data['all-links'].extend(all_links)
    recursively_data['own-links'].extend(own_links)
    for link in own_links:
        recursive_link_collector(link)