import mimetypes
from urllib.request import urlopen
import requests
import json
from string import printable
from bs4 import BeautifulSoup
import re
import time
import string

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

# TEST, check response time
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

# TEST, check link text length
def check_link_text_length(link_texts, max_length):
    exceed_link_texts = {}
    for link_text in link_texts.values():
        if len(link_text) > max_length:
            exceed_link_texts[link_text] = len(link_text)
    return exceed_link_texts

# TEST, check special characters on link texts
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

# TEST, check viewport
def check_viewport(links):
    viewport_link = {}
    for link in links:
        viewport = 0
        page = urlopen(link)
        page_soup = BeautifulSoup(page, "lxml")
        for meta in page_soup.find_all('meta'):
            metaname = meta.get('name', '').lower()
            if 'viewport' == metaname:
                viewport = 1
        if viewport <= 0:
            viewport_link[link] = 'not meta viewport'
    return viewport_link

# TEST, check Content-type
def check_content_type(links):
    content_type_link = {}
    for link in links:
        content_type = 0
        page = urlopen(link)
        page_soup = BeautifulSoup(page, "lxml")
        for meta in page_soup.find_all('meta'):
            metaname = meta.get('http-equiv', '').lower()
            if 'content-type' == metaname:
                content_type = 1
        if content_type <= 0:
            content_type_link[link] = 'not meta content_type'
    return content_type_link

# TEST, check description
def check_description(links):
    description_link = {}
    for link in links:
        description = 0
        page = urlopen(link)
        page_soup = BeautifulSoup(page, "lxml")
        for meta in page_soup.find_all('meta'):
            metaname = meta.get('name', '').lower()
            if 'description' == metaname:
                description = 1
        if description <= 0:
            description_link[link] = 'not meta description'
    return description_link

# TEST, check language
def check_language(links):
    language_link = {}
    for link in links:
        language = 0
        page = urlopen(link)
        page_soup = BeautifulSoup(page, "lxml")
        for meta in page_soup.find_all('meta'):
            metaname = meta.get('name', '').lower()
            if 'language' == metaname:
                language = 1
        if language <= 0:
            language_link[link] = 'not meta language'
    return language_link

# TEST, check robots
def check_robots(links):
    robots_link = {}
    for link in links:
        robots = 0
        page = urlopen(link)
        page_soup = BeautifulSoup(page, "lxml")
        for meta in page_soup.find_all('meta'):
            metaname = meta.get('name', '').lower()
            if 'robots' == metaname:
                robots = 1
        if robots <= 0:
            robots_link[link] = 'not meta robots'
    return robots_link

# TEST, check keywords
def check_keywords(links):
    keywords_link = {}
    for link in links:
        keywords = 0
        page = urlopen(link)
        page_soup = BeautifulSoup(page, "lxml")
        for meta in page_soup.find_all('meta'):
            metaname = meta.get('name', '').lower()
            if 'keywords' == metaname:
                keywords = 1
        if keywords <= 0:
            keywords_link[link] = 'not meta keywords'
    return keywords_link

# TEST, check title control
def check_title_control(links):
    title_link = {}
    for link in links:
        title = ''
        title_count = 0
        title_count2 = 0
        page = urlopen(link)
        page_soup = BeautifulSoup(page, "lxml")
        for meta in page_soup.find_all('meta'):
            metaname = meta.get('name', '').lower()
            title = page_soup.title.string
            if 'description' == metaname:
                metacontent = meta.get('content', '')
                title_count = metacontent.count(title)
            elif 'keywords' == metaname:
                metacontent = meta.get('content', '')
                title_count2 = metacontent.count(title)
        if (title_count <= 0 and title_count2 <= 0):
            title_link[link] = page_soup.title.string
    return title_link

# TEST, check file_length
def check_file_length(links):
    file_length_link = {}
    for link in links:
        filedata = urlopen(link)
        data = filedata.length
        if(data>1000):
            file_length_link[link] = 'file size should be printed'
        #a=wget.download('http://i3.ytimg.com/vi/J---aiyznGQ/mqdefault.jpg', '')
        #a=urllib.request.urlretrieve('//www.cdn.renault.com/content/dam/Renault/TR/global-brochures/Clio-Kasim-2019.pdf')
        #print(a)
    return file_length_link

# TEST, check internet_time_out
def check_internet_time_out(links,time_out_max):
    internet_time_out_link = {}
    for link in links:
        t0 = time.time()
        try:
            with urlopen(link) as response:
                html = response.read()
        except:
            continue
        t1 = time.time()
        total = t1 - t0
        if(total > time_out_max):
            internet_time_out_link[link] = 'Sites for more than ' + str(time_out_max) + ' seconds'
    return internet_time_out_link

# TEST, check file_type
def check_file_type(links):
    file_type = {'.pdf', '.png', '.doc'}
    file_type_link = {}
    sayi=0
    for link in links:
        #link = 'https://www.w3schools.com/tags/tryit.asp?filename=tryhtml5_a_download2'
        try:
            page = urlopen(link)
            page_soup = BeautifulSoup(page, "lxml")
        except:
            continue
        for file in page_soup.find_all('a'):
            classname = file.get('download', '').lower()
            if '' != classname:
                file_link = file.get('href', '')
                for type in file_type:
                    if ((file_link.count(type)) > 0):
                        sayi=sayi+1
                if(sayi<=0):
                    file_type_link[file_link] = 'out of designated extensions'
    return file_type_link

# Her sayfada bir ana sayfa linki olup olmadığını kontrol eden test
def check_anasayfa_link(links):
    for link in links:
        page = urlopen(link)
        page_soup = BeautifulSoup(page, "lxml")
        allatags = page_soup.find_all('a')
        for tags in allatags:
            if "Ana Sayfa" or "anasayfa" or "Ana Sayfa" or "Anasayfa" in tags:
                print("Ana Sayfa bağlantısı var.")
                return True
            else:
                print("Ana Sayfa bağlantısı yok.")
                return False

#Diğer fonksiyonlarda kullanılmak için sanırım.
def has_special_char(text: str) -> bool:
    if set(text).difference(string.ascii_letters + string.digits):
        return True
    else:
        return False
"""
def has_special_char(text: str) -> bool:
    return any(c for c in text if not c.isalnum() and not c.isspace())
"""
# TODO Bu array i Yaml a taşımak gerekir.
baglaclar = ["ama", "fakat", "lâkin", "ancak", "yalnız", "oysa", "oysaki", "hâlbuki",
             "ve", "ile", "ki", "de", "çünkü", "zira", "madem", "mademki",
             "veyahut", "yahut", "veya", "ya da", "şayet", "eğer", "ise", "öyleyse",
             "o halde", "kısacası", "demek ki", "nitekim", "yoksa", "anlaşılan", "hatta", "üstelik",
             "ayrıca", "hem", "hem de", "yine", "gene", "meğer"
             ]

# Başlıkta özel karakter ve bağlaç olup olmadığını kontrol eden test
def check_title_for_special_characters_and_baglaclar(url):
    page = urlopen(url)
    page_soup = BeautifulSoup(page, "lxml")
    if has_special_char(page_soup.title.string):
        print("Sayfa başlığında özel karakter bulunmakta.")
    else:
        print("Sayfa başlığında özel karakter bulunmamakta.")
    for baglac in baglaclar:
        if baglac in page_soup.title.string.lower():
            baglac_var = True
            break
        else:
            baglac_var = False
    if baglac_var:
        print("Başlıkta bağlaç var.")
    else:
        print("Başlıkta bağlaç yok.")

# Ana sayfada çok fazla sayıda bağlantıya yer verilmesinin,
# ana sayfa görünümünü karmaşık hale getireceği ve
# internet sitesinin kullanılabilirliğini azaltacağı göz önünde bulundurulmalıdır.
def check_mainpage_for_many_links(url, links_threshold):
    page = urlopen(url)
    page_soup = BeautifulSoup(page, "lxml")
    allatags = page_soup.find_all('a')
    if len(allatags) >= links_threshold:
        print("Ana sayfada çok fazla sayıda bağlantı var. Link sayısı:" + str(len(allatags)))
    else:
        print("Ana sayfada çok fazla sayıda bağlantı yok. Link sayısı:" + str(len(allatags)))

# Ana sayfaya, her sayfada bulunan kurum logosu tıklanarak gidilebilmelidir
# ancak bu yöntem ana sayfaya gitmek için tek yol olarak görülmemelidir. -> Barış
def check_pages_for_logolink_to_mainpage(all_urls):
    for url in all_urls:
        page = urlopen(url)
        page_soup = BeautifulSoup(page, "lxml")
        links = page_soup.find_all('a')
        for link in links:
            lgs = link.find_all('img', re.compile("logo"))
            print(lgs)
        """for links in page_soup.find_all('a'):
            if len(links.findChildren(attrs={'id': 'logo', 'name': 'logo', 'class': 'logo'})) > 0:
                result = True
            else:
                result = False
    if result:
        print("Ana sayfaya, her sayfada bulunan kurum logosu tıklanarak gidilebiliyor")
    else:
        print("Ana sayfaya, her sayfada bulunan kurum logosu tıklanarak gidilemiyor")"""