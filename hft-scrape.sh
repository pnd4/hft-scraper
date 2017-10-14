#!/bin/bash

echo 'SCRAPING..'

python hft-scrape-root.py
python hft-scrape-savings.py
python hft-scrape-extra.py
python hft-scrape-digital.py
python hft-scrape-email.py
echo 'DONE SCRAPING\n'

# Merge seperate CSVs into hft-spreadsheet-raw.csv
echo 'MERGING..'
cat csv/hft-spreadsheet-root.csv > csv/hft-spreadsheet-raw.csv
cat csv/hft-spreadsheet-savings.csv >> csv/hft-spreadsheet-raw.csv
cat csv/hft-spreadsheet-extra.csv >> csv/hft-spreadsheet-raw.csv
cat csv/hft-spreadsheet-digital.csv >> csv/hft-spreadsheet-raw.csv
cat csv/hft-spreadsheet-email.csv >> csv/hft-spreadsheet-raw.csv
echo 'DONE MERGING\n'

# Remove dupes and sort
echo 'REMOVING DUPES AND SORTING..'
python hft-csv.py
echo 'DONE REMOVING DUPES AND SORTING\n'
