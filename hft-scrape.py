## HFT Coupon Scraper (hft-scrape.py)
# by Kevin 'pnd4' Tran

#!/usr/bin/python

import requests
import urllib
import re
from bs4 import BeautifulSoup

url = "https://www.harborfreight.com/savings_coupons.html"

r = requests.get(url)

if r.status_code != 200:
    print("ERROR: Request Denied")
else:
    print("item" + "|" + "skus" + "|" + "desc" + "|" + "code")

soup = BeautifulSoup(r.text, "lxml")

## Find all <div> elements belonging to a 'coupon-container*' class, each is a coupon
coupons = soup.find_all("div", re.compile("coupon-container*"))

## Create dict to store data-groups
## - catalog[0] = "12345"                                   -> dict-key, the items sku
## - catalog[0]["desc"] = "4in Angle Grinder"               -> the sku's desc
## - catalog[0]["barcode"] = "https://hft.com/12345.jpg"    -> coupon-barcode url
## - catalog[0]["code"] = "987654321"                       -> coupon-code
catalog = {}

## Go through all items and use each sku as a 'key'
## 
for coupon in coupons:
    sku = coupon.find("a", attrs={"target": "_blank"})["href"].split("-")[-1].split(".")[-2]
    catalog[sku] = {}
    catalog[sku]["skus"] = (sku, )
    catalog[sku]["desc"] = coupon.img["alt"]
    catalog[sku]["barcode"] = coupon.find("img", attrs={"width": "188"})["src"]
    catalog[sku]["code"] = catalog[sku]["barcode"].split("/")[-1].split(".")[-2]

### 
#print("[Example]\n\nItem: " + "63268" + "\nCode: " + catalog['62368']["code"] + "\nDesc: " + catalog['62368']["desc"] + "\n")

###
#print("[Dict Node]\n",catalog['62368'], "\n\n")

## Print data from the Catalog
for product in catalog:
    print('"' + product + '"|"', end='')
    for aggsku in catalog[product]["skus"]:
        print(aggsku + ",", end='')
    print('"|"' + catalog[product]["desc"] + '"|"' + catalog[product]["code"] + '"')

