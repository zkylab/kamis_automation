import infra
import tests
import yaml
from json2html import *

with open(r'C:\Users\Burak\Desktop\kamis_automation-master\properties.yaml') as file:
    properties_list = yaml.load(file, Loader=yaml.FullLoader)
#all_urls = infra.get_all_links("http://turkiye.gov.tr")
liste =  ["http://isar.com.tr/","http://isar.com.tr/hakkimizda/","http://isar.com.tr/urunlerimiz/","http://isar.com.tr/hakkimizda/","http://isar.com.tr/urunlerimiz/","http://www.turkishtestingboard.org/istqb-sinavlar-hakkinda-bilgi/"]
#print(tests.check_link_len(all_urls['final_links'], 15))
#Modify code to get all links texts.
#print(tests.check_link_text_length(infra.all['link-text'], 10))
print(tests.check_title_repeat(liste))
print(tests.check_breadcrumbs_title(liste,properties_list.get('breadcrumb_class')))
print(tests.check_breadcrumbs(liste,properties_list.get('breadcrumb_class')))
print(tests.check_breadcrumbs_link(liste,properties_list.get('breadcrumb_class')))

print(tests.check_link_new_tab(liste))
print("test")