#!/usr/bin/env python3

import re
import csv
import sys
import argparse
from time import sleep
from pathlib import Path
from datetime import datetime

class QualysParser():

    def __init__(self, options):

        self.options    = options
        self.limit      = options.limit
        self.current    = 0

        self.pattern    = pattern = re.compile('[\W_]+')
        self.keywords   = [self.pattern.sub('', word) for word in options.keywords]

        self.fieldnames = ['IP', 'DNS', 'NetBIOS', 'OS', 'IP Status', 'QID', 'Title', 'Type', 'Severity', 'Port', 'Protocol', 'FQDN', 'SSL', 'CVE ID', 'Vendor Reference', 'Bugtraq ID', 'CVSS Base', 'CVSS Temporal', 'Threat', 'Impact', 'Solution', 'Exploitability', 'Associated Malware', 'Results', 'PCI Vuln', 'Instance']



    def parse_csv(self):

        counter = 0

        with open(str(self.options.csv), newline='') as f0:
            qualys_csv = csv.DictReader(f0, fieldnames=self.fieldnames)

            with open(str(options.write), newline='') as f1:
                output_csv = csv.DictWriter(f1, fieldnames=self.fieldnames)
                output_csv.writeheader()
                
                for row in qualys_csv:
                    try:
                        if int(row['Severity']) in self.options.severity:
                            if self.check_keyword(row):
                                if self.limit and self.current > self.limit:
                                    break
                                else:
                                    output_csv.writerow(row)
                                    self.current += 1

                    except (ValueError, KeyError):
                        continue

                    counter += 1
                    if counter % 100 == 0:
                        sys.stderr.write('[+] Processed {:,} lines\r'.format(str(counter)))


    def check_keyword(self, row):

        row = [self.pattern.sub('', i).lower() for i in row]

        for field in row:
            for word in self.keywords:
                if word in field:
                    return True

        return False


def keywords(s):

    if ',' in s:
        return [i.lower() for i in s.split(',')]
    else:
        return [s.lower()]



def severity(s):

    if ',' in s:
        return [int(i) for i in s.split(',')]
    elif '-' in s:
        a,b = s.split('-')[:2]
        return range(int(a), int(b+1))
    else:
        return [int(s)]


if __name__ == '__main__':

    default_filename = datetime.now().strftime('qualys_%H_%M_%d_%m_%S_%Y.csv')
    default_filename = Path.home() / 'Desktop' / default_filename

    parser = argparse.ArgumentParser(description='Filter Qualys scan results from CSV')
    parser.add_argument('-o',   '--overwrite',  action='store_true',                    help='overwrite destination file if it exists')
    parser.add_argument('-w',   '--write',      type=Path,  default=default_filename,   help='output file, default = {}'.format(str(default_filename)))
    parser.add_argument('-s',   '--severity',   type=severity,  default=range(0,6),     help='only output this severity - e.g. "1,3,5" or "4-5"')
    parser.add_argument('-k',   '--keywords',   type=keywords,                          help='only outputs lines matching this search term(s)')
    parser.add_argument('-l',   '--limit',      type=int,                               help='limit results, default = unlimited')
    parser.add_argument('csv',                                                          help='Qualys scan CSV')

    try:
        options = parser.parse_args()

        if not options.csv.isfile():
            print('[!] {} doesn\'t exist'.format(str(options.csv)))
            sleep(1)
            sys.exit(1)

            if options.write.exists() and not options.overwrite:
                print('[!] {} already exists.  Consider using --overwrite')
                sleep(2)
                sys.exit(1)

        q = QualysParser(options)
        q.parse_csv()

    except AssertionError as e:
        sys.stderr.write('[!] {}'.format(str(e)))
        sys.exit(1)
    except KeyboardInterrupt:
        sys.stderr.write('[!] Interrupted')
        sys.exit(1)