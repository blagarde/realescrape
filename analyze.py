from codecs import open as copen
from argparse import ArgumentParser
from json import load
from unicodecsv import writer
from collections import defaultdict
from unidecode import unidecode
import re


SCRAPED_FIELDS = "url price size description title postcode".split(' ')
ALL_FIELDS = SCRAPED_FIELDS + ['ppsqm']


class Property(dict):
 
    def __getattr__(self, key):
        if key in self:
            return self[key]
        return None
 
    def __setattr__(self, key, value):
        self[key] = value

    def display(self, blacklist):
        contents = unidecode(self.title.lower()) + unidecode(self.description.lower())
        return not any([regex.search(contents) is not None for regex in blacklist])


if __name__ == "__main__":
    ap = ArgumentParser(description="Analyze and filter JSON scraping output")
    ap.add_argument("-b", "--blacklist", type=str, default=None, help="A list of terms, one per line. Items containing any of them will be excluded")
    ap.add_argument("infile", type=str, help="Input JSON file")
    ap.add_argument("outfile", type=str, help="Output CSV file")
    args = ap.parse_args()
    
    blacklist = [] if args.blacklist is None else [re.compile(unidecode(l.rstrip('\n').lower())) for l in copen(args.blacklist, 'r', encoding='utf8')]

    of = open(args.outfile, 'w')
    ocsv = writer(of, delimiter='\t')
    ocsv.writerow(ALL_FIELDS)


    selected = 0
    with copen('out.json', 'r', encoding='utf8') as fh:
        properties = [Property(**dct) for dct in load(fh)]
        for p in properties:
            if p.display(blacklist):
                ocsv.writerow([p[f] for f in ALL_FIELDS])
                selected += 1
        total = len(properties)
        print "Total/selected/censored: %s/%s/%s" % (total, selected, total - selected)
    of.close()
