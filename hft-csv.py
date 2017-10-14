#! python3

import csv
import itertools
import operator

filename = 'csv/hft-spreadsheet-raw.csv'
outfile = 'csv/hft-spreadsheet-nodupes.csv'
ndupes = 0

with open(filename, 'r') as fin, open(outfile, 'w') as fout:
    fieldnames = ['sku', 'desc', 'code', 'save']
    dialect = csv.Sniffer().sniff(fin.read(1024))
    fin.seek(0)
    reader = csv.DictReader(fin, fieldnames=fieldnames, delimiter='|', quotechar='"')
    writer = csv.DictWriter(fout, fieldnames=fieldnames, dialect='excel', quotechar='"', delimiter='|', quoting=csv.QUOTE_ALL)
    try:
        writer.writeheader() 
        
        ## Sort by SKU
        sortResult = sorted(reader, key=lambda s: s['sku'])
        
        ## Remove duplicates
        entries = set()
        for srow in sortResult:
            key = (srow['sku'], srow['save'])
            if key not in entries:
                writer.writerow(srow)
                entries.add(key)
            else:
                print('Removed: ', srow)
                ndupes += 1
        
        print('Total duplicates removed:', ndupes)

    except csv.Error as e:
        sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
