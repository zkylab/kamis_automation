import infra
import tests
import yaml
with open(r'C:\Users\BCENGIZ\Desktop\kamis_automation-burakCengiz\properties.yml') as file:
    properties_list = yaml.load(file, Loader=yaml.FullLoader)
all_urls = infra.get_all_links("http://turkiye.gov.tr")
liste =  ["http://isar.com.tr/","http://isar.com.tr/hakkimizda/","http://isar.com.tr/urunlerimiz/","http://isar.com.tr/hakkimizda/","http://isar.com.tr/urunlerimiz/"]
print(tests.check_breadcrumbs_title(liste,properties_list.get('breadcrumb_class')))
#print(tests.check_link_len(all_urls['final_links'], 15))
#Modify code to get all links texts.
#print(tests.check_link_text_length(infra.all['link-text'], 10))
print("test")