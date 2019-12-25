import mimetypes
from urllib.request import urlopen

import requests
from PIL.ImageFile import ImageFile
from bs4 import BeautifulSoup
import urllib
from mimetypes import MimeTypes

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


def check_link_text_length(link_texts, max_length):
    exceed_link_texts = {}
    for text in link_texts:
        if len(text) > max_length:
            # TODO: store link in dict, not len of text
            exceed_link_texts['link-text'] = len(text)
    return exceed_link_texts

#Alt sayfalarda, zamandan tasarruf ve hızlı erişim imkânı sunan ekmek kırıntısı (breadcrumbs) yapısı kullanılmalıdır.
def check_breadcrumbs(liste, bread_crumb_class_name):
    for link in liste:
        page = urlopen(link)
        page_soup = BeautifulSoup(page, "lxml")
        bread_crumb_element = page_soup.find("", {"class": bread_crumb_class_name})
        if bread_crumb_element is not None:
            print(page_soup.title)
            print("BreadCrumb var")
        else:
            print(page_soup.title)
            print("BreadCrumb yok")
    return bread_crumb_element

#Site içindeki tüm sayfalarda aynı başlıkların kullanılmasından kaçınılmalı, her sayfaya özel ve sayfa içeriğini tanımlayıcı bir başlık seçilmelidir.
def check_title_repeat(liste):
    titles_on_the_site =[]
    repeated_titles=["Tekrar eden başlıklar : "]
    for link in liste:
        count=0
        page = urlopen(link)
        page_soup = BeautifulSoup(page, "lxml")
        #print(page_soup.title.text)
        titles_on_the_site.append(page_soup.title.text)
        for title in titles_on_the_site:
            if title == page_soup.title.text:
                count = count+1
            if(count>1):
                repeated_titles.append(title)
    if(count<=1):
        repeated_titles.append("Yoktur.")


    return repeated_titles

#Ekmek kırıntısı yapısı içindeki hiyerarşik yolun en sonundaki bölüm kullanıcıların bulunduğu sayfayı göstermelidir.
def check_breadcrumbs_title(liste, bread_crumb_class_name):
    for link in liste:
        page = urlopen(link)
        page_soup = BeautifulSoup(page, "lxml")
        print("*****************************************************")
        print("EKMEK KIRINTISI VE BAŞLIK İLİŞKİSİ Kontrol edilen sayfa başlığı : " + page_soup.title.text)
        for bc_list in page_soup.findAll('', class_=bread_crumb_class_name):
            for list_items in bc_list.findAll('li'):
                list_link_items = bc_list.findAll('a')
            if list_items.text in page_soup.title.text:
                print(page_soup.title)
                print("Ekmek kırıntısı sonundaki bölüm sayfa başlığı ile uyumlu")
            else:
                print(page_soup.title)
                print("Ekmek kırıntısı sonundaki bölüm sayfa başlığı ile uyumlu DEĞİL")
                print("Sayfa Başlığı : " + page_soup.title.text)
                print("Ekmek kırıntısı sonu : " + list_items.text)

#Hiyerarşik yolun en sonundaki bölümün tıklanabilir olmaması gerekmektedir.
def check_breadcrumbs_link(liste,bread_crumb_class_name):
    for link in liste:
        page = urlopen(link)
        page_soup = BeautifulSoup(page, "lxml")
        print("*****************************************************")
        print("EKMEK KIRINTISI BAĞLANTI DURUMU Kontrol edilen sayfa başlığı : "+page_soup.title.text)
        for bc_list in page_soup.findAll('', class_=bread_crumb_class_name):
            for list_link_items in bc_list.findAll('a'):
                print("")
            for list_items in bc_list.findAll('li'):
                list_link_items = bc_list.findAll('a')
            if list_link_items is list_items:
                print("Breadcrumb ın sonunda link var : !! "+list_items.text)
            else:
                print("Breadcrumbda sonda link yok yalnızca : "+list_items.text)
def collect_pdfs(liste):
    pdfs =[]
    for link in liste:
        page = urlopen(link)
        page_soup = BeautifulSoup(page, "lxml")
        for links in page_soup.findAll('a'):
            type = mimetypes.guess_type(links.get("href"))
            print(type[0])
            text = type[0]
            if text is not "None":
                print(type)

    return pdfs

def check_link_new_tab(liste):
    links_open_in_new_tab =["Yeni Sekmede Açılan Dosyalar :"]
    links_not_open_in_new_tab =["text/html Olmamasına Rağmen Yeni Sekmede Açılmayan Dosyalar :"]
    for link in liste:
        page = urlopen(link)
        page_soup = BeautifulSoup(page, "lxml")
        for links in page_soup.findAll('a'):

            if links.get('href').startswith("http:"):
                test_links = urlopen(links.get('href'))
                content_type_of_tested = test_links.headers['Content-Type']
                print("content : " + content_type_of_tested + "  :" + links.get('href'))
                if not content_type_of_tested.startswith("text/html"):
                    tag_test_for_new_tab = links.get('target')
                    print(tag_test_for_new_tab)
                    if tag_test_for_new_tab == "_blank":
                        links_open_in_new_tab.append(links.get('href'))
                    else:
                        links_not_open_in_new_tab.append(links.get('href'))
    return links_open_in_new_tab,links_not_open_in_new_tab
