import infra
import tests

all_urls = infra.get_all_links("http://turkiye.gov.tr")
print(tests.check_link_len(all_urls['final_links'], 15))
