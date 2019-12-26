import infra
import tests

all_urls = infra.get_all_links("https://www.turkiye.gov.tr")
print(all_urls['final_links'])
print(tests.check_link_len(all_urls['final_links'], 15))
#Modify code to get all links texts.
#print(tests.check_link_text_length(infra.all['link-text'], 10))

"""tests.check_anasayfa_link(infra.baseUrl)
tests.check_title_for_special_characters_and_baglaclar(infra.baseUrl)"""
#tests.check_mainpage_for_many_links(infra.baseUrl, 104)
tests.check_pages_for_logolink_to_mainpage(all_urls['final_links'])