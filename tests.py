import mimetypes
from urllib.request import urlopen

import requests
import json
from string import printable
from bs4 import BeautifulSoup

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
def check_title_len(titles, title_size_max):
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

#Alt sayfalarda, zamandan tasarruf ve hızlı erişim imkânı sunan ekmek kırıntısı (breadcrumbs) yapısı kullanılmalıdır.
def check_breadcrumbs(liste, bread_crumb_class_name):
    page_with_breadcrumb =["Ekmek kırıntısı olan sayfalar : "]
    page_without_breadcrumb =["Ekmek kırıntısı olmayan sayfalar : "]
    for link in liste:
        page = urlopen(link)
        page_soup = BeautifulSoup(page, "lxml")
        bread_crumb_element = page_soup.find("", {"class": bread_crumb_class_name})
        if bread_crumb_element is not None:
            page_with_breadcrumb.append(page_soup.title)
        else:
            page_without_breadcrumb.append(page_soup.title)
    return page_without_breadcrumb,page_with_breadcrumb

#Site içindeki tüm sayfalarda aynı başlıkların kullanılmasından kaçınılmalı, her sayfaya özel ve sayfa içeriğini tanımlayıcı bir başlık seçilmelidir.
def check_title_repeat(liste):
    titles_on_the_site =[]
    repeated_titles=["Tekrar eden başlıklar" ":"]
    repeated_titles_dict = {'Test Başlığı' : 'Repeated Titles'}
    count = 0
    for link in liste:
        count = 0
        page = urlopen(link)
        page_soup = BeautifulSoup(page, "lxml")
        titles_on_the_site.append(page_soup.title.text)
        for title in titles_on_the_site:
            if title == page_soup.title.text:
                count = count+1
            if(count>1):
                repeated_titles.append(title)
                key = title
                value = "Tekrar Eden Başlık"
                repeated_titles_dict[key]=value
    if(count<=1):
        repeated_titles.append("Yoktur.")
    return repeated_titles

#Ekmek kırıntısı yapısı içindeki hiyerarşik yolun en sonundaki bölüm kullanıcıların bulunduğu sayfayı göstermelidir.
def check_breadcrumbs_title(liste, bread_crumb_class_name):
    title_breadcrumb_same =["Başlıkta ekmek kırıntısının son öğesi olan sayfalar : "]
    title_breadcrumb_same_dict={'Test Başlığı ':'Başlıkta ekmek kırıntısının son öğesi olan sayfalar'}
    title_breadcrumb_diff =["Başlıkta ekmek kırıntısının son öğesi olmayan sayfalar : "]
    title_breadcrumb_diff_dict={'Test Başlığı ':'Başlıkta ekmek kırıntısının son öğesi olmayan sayfalar'}
    for link in liste:
        page = urlopen(link)
        page_soup = BeautifulSoup(page, "lxml")
        for bc_list in page_soup.findAll('', class_=bread_crumb_class_name):
            for list_items in bc_list.findAll('li'):
                list_link_items = bc_list.findAll('a')
            if list_items.text in page_soup.title.text:
                key = page_soup.title.text
                value = "Ekmek kırıntısının sonu başlık içinde yer almıyor"
                title_breadcrumb_same_dict[key]=value
                title_breadcrumb_same.append(page_soup.title)
            else:
                key = page_soup.title.text
                value = "Ekmek kırıntısının sonu başlık içinde yer alıyor"
                title_breadcrumb_diff_dict[key] = value
                title_breadcrumb_diff.append(page_soup.title)
    return  title_breadcrumb_diff,title_breadcrumb_same

#Hiyerarşik yolun en sonundaki bölümün tıklanabilir olmaması gerekmektedir.
def check_breadcrumbs_link(liste,bread_crumb_class_name):
    last_breadcrumb_with_link =["Ekmek kırıntısının sonunda link olan sayfalar : "]
    last_breadcrumb_without_link = ["Ekmek kırıntısının sonunda link olmayan sayfalar : "]
    for link in liste:
        page = urlopen(link)
        page_soup = BeautifulSoup(page, "lxml")
        for bc_list in page_soup.findAll('', class_=bread_crumb_class_name):
            for list_items in bc_list.findAll('li'):
                list_link_items = bc_list.findAll('a')
            if list_link_items is list_items:
                last_breadcrumb_with_link.append(page_soup.title)
            else:
                last_breadcrumb_without_link.append(page_soup.title)
    return last_breadcrumb_with_link,last_breadcrumb_without_link

#Yeni Sekmede açılan - açılmayan linkler
def check_link_new_tab(liste):
    links_open_in_new_tab =["Yeni Sekmede Açılan Dosyalar :"]
    links_not_open_in_new_tab =["text/html Olmamasına Rağmen Yeni Sekmede Açılmayan Dosyalar :"]
    for link in liste:
        page = urlopen(link)
        page_soup = BeautifulSoup(page, "lxml")
        for links in page_soup.findAll('a'):
            if links.get('href') is not None:
                if links.get('href').startswith("http:"):
                    test_links = urlopen(links.get('href'))
                    content_type_of_tested = test_links.headers['Content-Type']
                    if not content_type_of_tested.startswith("text/html"):
                        tag_test_for_new_tab = links.get('target')
                        if tag_test_for_new_tab == "_blank":
                            links_open_in_new_tab.append(links.get('href'))
                        else:
                            links_not_open_in_new_tab.append(links.get('href'))
    return links_open_in_new_tab,links_not_open_in_new_tab
