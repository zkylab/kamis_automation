import infra
import tests
import yaml
with open(r'C:\Users\Burak\Desktop\kamis_automation-master\properties.yaml') as file:
    properties_list = yaml.load(file, Loader=yaml.FullLoader)
baseUrl ="http://isar.com.tr/"
infra.recursive_link_collector(baseUrl)
own_links = infra.recursively_data['own-links']
images = infra.recursively_data['images']
link_titles = infra.recursively_data['link-title']
all_links = infra.recursively_data['all-links']
link_texts = infra.recursively_data['link-texts']

# TESTS. Will not be printed, reported...
'''
print(tests.check_image_size(images, properties_list.get('image_size_max')))
print(tests.check_link_len(all_links, properties_list.get('link_size_max')))
print(tests.check_title_len(link_titles, properties_list.get('title_size_max')))
print(tests.check_response_time(own_links, properties_list.get('response_time_max')))
print(tests.check_link_text_length(link_texts, properties_list.get('max_length')))
print(tests.check_special_character(link_texts))
print(tests.check_title_repeat(own_links))
print(tests.check_breadcrumbs_title(own_links,properties_list.get('breadcrumb_class')))
print(tests.check_viewport(all_links))
print(tests.check_content_type(all_links))
print(tests.check_description(all_links))
print(tests.check_language(all_links))
print(tests.check_robots(all_links))
print(tests.check_keywords(all_links))
print(tests.check_title_control(all_links))
print(tests.check_file_length(all_links))
print(tests.check_internet_time_out(all_links,2))
print(tests.check_file_type(all_links))
print(tests.check_breadcrumbs(own_links,properties_list.get('breadcrumb_class')))
print(tests.check_link_new_tab(own_links))
print(tests.check_title_brand_name(link_titles, properties_list.get('kurum_adi')))
'''
print(tests.check_title_Anasayfa(baseUrl))
