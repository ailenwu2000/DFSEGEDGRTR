# -*- coding=utf-8 -*-
import requests
from lxml import etree
import io
import sys
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
url = 'http://warrants-hk.credit-suisse.com/gb/warrants/search_gb.cgi?order=dbcode_desc&ucode=HSI&sname=CS&industry=&wtype=ALL&egear=0&mtype=0&osp=0&inout=0&premium=0'

rep = requests.get(url)
# print(type(rep.content), rep.content)
text = rep.content.decode('utf-8')
tree = etree.HTML(text)
# nodes = tree.xpath("//div[@class='scrollingInside']//table//tbody//tr//td")
nodes = tree.xpath("//select[@name='ucode']/option")
for node in nodes:
    print(node.text)


