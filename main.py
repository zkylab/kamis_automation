import infra
import tests

baseUrl = "https://www.antalyalinakliyat.com.tr/"
infra.recursive_link_collector(baseUrl)

own_links = infra.recursively_data['own-links']
images = infra.recursively_data['images']
link_titles = infra.recursively_data['link-title']
all_links = infra.recursively_data['all-links']
link_texts = infra.recursively_data['link-texts']

# TESTS. Will not be printed, reported...
print(tests.check_image_size(images, 15))
print(tests.check_link_len(all_links, 10))
print(tests.check_title_len(link_titles, 10))
print(tests.check_response_time(own_links, 10))
print(tests.check_link_text_length(link_texts, 20))
print(tests.check_special_character(link_texts))
