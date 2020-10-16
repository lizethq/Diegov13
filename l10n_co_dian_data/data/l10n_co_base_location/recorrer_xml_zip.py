from lxml import etree
import os

XMLpath = os.path.dirname(os.path.abspath(__file__)) + '/res_better_zip_data.xml'
request = etree.parse(XMLpath)

root = request.getroot()

for element in root.iter():
    # print(element.tag, element.attrib)
    if element.tag == 'field' and element.attrib.get('name') == 'code':
        print(element.text, element.getparent().attrib)
        city = etree.SubElement(element.getparent(), 'field', name='city_id', ref='l10n_co_dian_data.res_city_co_' + element.text)
        # city.attrib = { 'name': 'city_id', 
        #                 'ref': 'l10n_co_dian_data.res_city_co_' + element.text}
        print(city.tag, city.attrib)

root_str = etree.tostring(root, pretty_print=True, encoding='utf-8')
file = open('zips.xml', 'wb')
file.write(root_str)