#!/usr/bin/python

## Spit out the data-set of our file.
import csv
with open('hft.csv', 'r') as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read(1024))
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect, delimiter='|', quotechar='"')
    try:
        for row in reader:
            print(row)
    except csv.Error as e:
        sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
