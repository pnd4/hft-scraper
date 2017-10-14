## HFT Digital Coupon Scraper (hft-scrape-digital.py)
# by Kevin 'pnd4' Tran

#! python3

import requests, re, urllib, csv
from bs4 import BeautifulSoup

def findAggSkus():
    # Aggregate SKUs
    aQuery = '"' + cFilter(cDesc) + '"'
    aUrl = "/catalogsearch/result/index/?q="
    
    # Request aggregate-sku page
    aRes = requests.get(prefix + aUrl + aQuery)
    try:
        aRes.raise_for_status()
    except requests.packages.urllib3.exceptions.MaxRetryError as e:
        print("Request failed. Status code: ", aRes.status_code())
        sitecheck(prefix + aUrl + aQuery)
    
    # Create aggregate-sku soup
    aSoup = BeautifulSoup(aRes.text, "lxml")
    
    # Work on each element
    aElements = aSoup.select('li[class^="item"]')
    for aElement in aElements:
        # Harvest aggregate-skus
        aSku = aElement.select_one('div[class="product-ids"]').get_text().split('#')[1]
        
        # Harvest regular-prices
        aPriceReg = aElement.select_one('span[id^="product-price"]').get_text().split('$')[1].strip(' ')
        
        # Assure coupon-code applies
        if aPriceReg == cPriceReg:
            print('\t' + aSku, '|', cDesc, '|', cCode, '|', cSave)
            # Write a row for each aSku into csvFile
            csvWriter.writerow([aSku, cDesc, cCode, cSave])
        else:
            print('[' + aSku + ']:', aPriceReg, '!=', cPriceReg)

    # Done with aggregate-sku page
    aSoup.decompose()
    aRes.close()

# Remove restrictive keywords
def cFilter(cString):
    words = ["X-Large", "Small", "Medium", "Large", "EPA/CARB", "EPA", "CARB", "SAE", "Metric"]
    words == [" - ", ","]
    for word in words:
        cString = cString.replace(word, '"+"')
    return cString

# Handle DNS Errors by continuing onto next element
def sitecheck(url):
    status = None
    message = ''
    try:
        resp = requests.head(url)
        status = str(resp.status_code)
    except requests.exceptions.NewConnectionError as exc:
        # filtering DNS lookup error from other connection errors
        # (until https://github.com/shazow/urllib3/issues/1003 is resolved)
        if type(exc.message) != requests.packages.urllib3.exceptions.MaxRetryError:
            raise
        reason = exc.message.reason    
        if type(reason) != requests.packages.urllib3.exceptions.NewConnectionError:
            raise
        if type(reason.message) != str:
            raise
        if ("[Errno 11001] getaddrinfo failed" in reason.message or     # Windows
            "[Errno -2] Name or service not known" in reason.message or # Linux
            "[Errno 8] nodename nor servname " in reason.message):      # OS X
            message = 'DNSLookupError'
        else:
            raise
    return url, status, message

# Open csv-file for write
csvFile = open('csv/hft-spreadsheet-digital.csv', 'w')
csvWriter = csv.writer(csvFile, dialect='excel', quotechar='"', delimiter='|', quoting=csv.QUOTE_ALL)

# URL partitions
u = '/digitalsavings.html'
prefix = 'http://harborfreight.com'

# Download the page.
res = requests.get(prefix + u)
try:
    res.raise_for_status()
except Exception as exc:
    print('There was a problem: %s' % (exc))

# Create soup
s = BeautifulSoup(res.text, 'lxml')

# Find all coupons
cpns = []
links = s.select('div[class="grid_1"] a[href^="/"]')
for cp in links:
    cp.img.decompose()
    cpns.append(cp)

if cpns == []:
    print("Could not find a coupon element.")
else:
    print("Found ", len(cpns), " coupons.\n")
    print("--------------- Begin --------------")
    for c in cpns:
        try:
            # Print current coupon
            print("\nCoupon:", cpns.index(c) + 1)
            
            # Gather coupon-item's URL
            cUrl = c['href']

            # Request coupon-page
            cRes = requests.get(prefix + cUrl)
            try:
                cRes.raise_for_status()
            except requests.packages.urllib3.exceptions.MaxRetryError as e:
                print("Request failed. Status code: ", cRes.status_code())
                sitecheck(prefix + cUrl)
            
            # Create coupon-page soup
            cSoup = BeautifulSoup(cRes.text, 'lxml')
            
            # Harvest coupon-description
            cDesc = cSoup.select_one('meta[property="og:title"]')['content']

            # Harvest coupon-code
            cCode = cSoup.select_one("#pricematching_price_coupon_code").string
            
            # Calculate savings
            cPriceReg = cSoup.select_one('meta[property="og:price:amount"]')['content']
            cPriceSale = cSoup.select_one("#pricematching_price_value").string
            cSave = "{:.2f}".format(float(cPriceReg) - float(cPriceSale))

            # Done with coupon page.
            cSoup.decompose()
            cRes.close()

            # Call findAggSkus function
            findAggSkus()
    
        except:
            continue

s.decompose()
res.close()
csvFile.close()

print("--------------- Done ---------------")
