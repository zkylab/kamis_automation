import infra
import tests

all_urls = infra.get_all_links("http://turkiye.gov.tr")
print(tests.check_link_len(all_urls['final_links'], 15))
#Modify code to get all links texts.
print(tests.check_link_text_length(infra.all['link-text'], 10))
