import requests
from text_wc_2 import *
from lxml import etree
xml = """<?xml version='1.0' encoding='utf-8'?>
<name>Seattle Sounders</name>"""
headers = {'Content-Type': 'application/xml'} # set what your server accepts
res = requests.post('https://www.sos.wa.gov/corps/search_results.aspx?name_type=starts_with&name=Seattle+Sounders&version=2&format=xml') #, data=xml, headers=headers)
#text_wc(res, 'xmlres.txt')
