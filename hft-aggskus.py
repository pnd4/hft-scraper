#!/usr/bin/python

import requests
import urllib
from bs4 import BeautifulSoup

q_keyword = '"2500 lb. ATV/Utility Electric Winch with Wireless Remote Control"'
q_url = "https://www.harborfreight.com/catalogsearch/result/index/?q="

r = requests.get(q_url + q_keyword)

s = BeautifulSoup(r.text, "lxml")

clones = s.find_all("div", class_="product-ids")

for clone in clones:
    print(clone.get_text().split("#")[1])
