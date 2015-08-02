# -*- coding=utf-8 -*-
import requests
from lxml import etree
import io
import sys
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
# url = 'http://warrants-hk.credit-suisse.com/gb/warrants/search_gb.cgi?order=dbcode_desc&ucode=HSI&sname=CS&industry=&wtype=ALL&egear=0&mtype=0&osp=0&inout=0&premium=0'
url = 'http://warrants-hk.credit-suisse.com/gb/warrants/search_gb.cgi'
# url = 'http://httpbin.org/get'
payload = {'order': 'dbcode_desc', 'ucode': '', 'sname': '',
           'industry': '', 'wtype': 'ALL',
           'egear': 0, 'mtype': 0, 'osp': 0,
           'inout': 0, 'premium': 0}
headers = {"User-Agent":
    "Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13"}
rep = requests.get(url, params=payload, headers=headers)

print(rep.url)
#print(rep.text)

# print(type(rep.content), rep.content)
text = rep.content.decode('utf-8')
tree = etree.HTML(text)
# nodes = tree.xpath("//div[@class='scrollingInside']//table//tbody//tr//td")
nodes = tree.xpath("//select[@name='ucode']/option")
for node in nodes:
    text = node.text
    if text.find(' ') > 0:
        print(text)
        (k, v) = node.text.split(' ')
        k = k[1:len(k)-1]

        print(k, v.encode('utf-8'))
