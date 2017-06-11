#! python3
# hft-scrape.py

import requests, re, urllib, csv
from bs4 import BeautifulSoup

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

# URL partitions
u = '/savings_coupons.html'
prefix = 'http://harborfreight.com'

# Download the page.
res = requests.get(prefix + u)
try:
    res.raise_for_status()
except Exception as exc:
    print('There was a problem: %s' % (exc))

# Create soup
s = BeautifulSoup(res.text, 'lxml')

# Find coupons
cpns = s.select('div[class^="coupon-container"]')
if cpns == []:
    print("Could not find a coupon element.")
else:
    print("Found ", len(cpns), " coupons.\n")
    
    # Open csv-file for write
    csvFile = open('hft-spreadsheet.csv', 'w')
    csvWriter = csv.writer(csvFile, dialect='excel', quotechar='"', delimiter='|', quoting=csv.QUOTE_ALL)
    for c in cpns:
        try:
            # Select item-description
            cText = c.img['alt']
            print('Desc=', cText)

            # Gather coupon-item's URL
            cUrl = c.a['href']

            # Extract coupon-item's SKU
            cSku = cUrl.split("-")[-1].split(".")[-2]

            # Request coupon-page
            cRes = requests.get(prefix + cUrl)
            try:
                cRes.raise_for_status()
            except requests.packages.urllib3.exceptions.MaxRetryError as e:
                print("Request failed. Status code: ", r.status_code())
                sitecheck(prefix + cUrl)
            
            # Create coupon-page soup
            rSoup = BeautifulSoup(cRes.text, 'lxml')
            
            # Harvest coupon-code
            cCode = rSoup.select_one("#pricematching_price_coupon_code").string
            print('CpnCode=', cCode)
            
            # Calculate savings
            cPriceReg = rSoup.select_one('meta[property="og:price:amount"]')['content']
            cPriceSale = rSoup.select_one("#pricematching_price_value").string
            cSave = "{:.2f}".format(float(cPriceReg) - float(cPriceSale))
            print('Savings=', cSave)

            # Clean-up
            rSoup.decompose()
            cRes.close()

            ## Aggregate SKUs
            cSkus = []
            aQuery = '"' + cText + '"'
            aUrl = "/catalogsearch/result/index/?q="
            aRes = requests.get(prefix + aUrl + aQuery)
            try:
                aRes.raise_for_status()
            except requests.packages.urllib3.exceptions.MaxRetryError as e:
                print("Request failed. Status code: ", r.status_code())
                sitecheck(prefix + aUrl + aQuery)
            aSoup = BeautifulSoup(aRes.text, "lxml")
            aSkus = aSoup.find_all("div", class_="product-ids")
            for aSku in aSkus:
                cSkus.append(aSku.get_text().split('#')[1])
            for itemNum in cSkus:
                csvWriter.writerow([itemNum, cText, cCode, cSave])
                print(itemNum, '|', cText, '|', cCode, '|', cSave)
            print()
            aSoup.decompose()
            aRes.close()
            
        except:
            pass
    csvFile.close()
s.decompose()
res.close()
# TODO: 

# TODO: Put all data on a row .. SKU | DESC | SAVE | CODE

# TODO: Sort data by sku

# TODO: Save data to CSV

print("--------------- Done. --------------")
