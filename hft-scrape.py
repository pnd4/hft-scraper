## HFT Coupon Scraper (hft-scraper.py)
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
    print("prod" + "|" + "sku" + "|" + "code")

soup = BeautifulSoup(r.text, "lxml")

## Find all <div> belonging to a 'coupon-container*' class
items = soup.find_all("div", re.compile("coupon-container*"))

## Create dict to store data-groups
## - catalog[0] = "4in Angle Grinder"                   -> key, containing data pairs
## - catalog[0]["sku"] = "12345"                        -> item-sku for 
## - catalog[0]["barcode"] = "https://hft.com/1234.jpg" -> coupon-barcode for '4in Angle Grinder'
catalog = {}

## Go through all items and use each '<img alt=>' string for a catalog.key
## Then use each barcode image's url as the barcode value for each key
##  
for item in items:
    catalog[item.img["alt"]] = {}
    catalog[item.img["alt"]]["sku"] = item.find("a", attrs={"target": "_blank"})["href"].split("-")[-1].split(".")[-2]
    catalog[item.img["alt"]]["barcode"] = item.find("img", attrs={"width": "188"})["src"]
    catalog[item.img["alt"]]["code"] = catalog[item.img["alt"]]["barcode"].split("/")[-1].split(".")[-2]

#print("\nCatalog\n\n", catalog, "\n\n")
for product in catalog.keys():
    print(product + "|" + catalog[product]["sku"] + "|" + catalog[product]["code"])
