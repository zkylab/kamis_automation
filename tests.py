from urllib.request import urlopen
import string
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


def check_link_text_length(link_texts, max_length):
    exceed_link_texts = {}
    for text in link_texts:
        if len(text) > max_length:
            # TODO: store link in dict, not len of text
            exceed_link_texts['link-text'] = len(text)
    return exceed_link_texts


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


baglaclar = ["ama", "fakat", "lâkin", "ancak", "yalnız", "oysa", "oysaki", "hâlbuki",
             "ve", "ile", "ki", "de", "çünkü", "zira",
             "madem", "mademki",
             "veyahut", "yahut", "veya", "ya da",
             "şayet", "eğer", "ise",
             "öyleyse", "o halde",
             "kısacası", "demek ki", "nitekim",
             "yoksa", "anlaşılan",
             "hatta", "üstelik", "ayrıca", "hem", "hem de",
             "yine", "gene",
             "meğer"
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


def has_special_char(text: str) -> bool:
    if set(text).difference(string.ascii_letters + string.digits):
        return True
    else:
        return False


"""
def has_special_char(text: str) -> bool:
    return any(c for c in text if not c.isalnum() and not c.isspace())
"""


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
        logos = page_soup.find_all(attrs={'id': 'logo', 'name': 'logo', 'class': 'logo'})
        print(logos)
        """for links in page_soup.find_all('a'):
            if len(links.findChildren(attrs={'id': 'logo', 'name': 'logo', 'class': 'logo'})) > 0:
                result = True
            else:
                result = False

    if result:
        print("Ana sayfaya, her sayfada bulunan kurum logosu tıklanarak gidilebiliyor")
    else:
        print("Ana sayfaya, her sayfada bulunan kurum logosu tıklanarak gidilemiyor")"""
