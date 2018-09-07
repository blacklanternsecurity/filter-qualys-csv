#!/usr/bin/env python3

import re
import csv
import sys
import argparse
from time import sleep
from pathlib import Path
from datetime import datetime

csv.field_size_limit(100000000)

class QualysParser():

    def __init__(self, options):

        self.options    = options
        self.limit      = options.limit
        self.current    = 0

        self.pattern    = re.compile('[\W_]+')
        self.keywords   = [self.pattern.sub('', word) for word in options.keywords]

        self.fieldnames = ['IP', 'DNS', 'NetBIOS', 'OS', 'IP Status', 'QID', 'Title', 'Type', 'Severity', 'Port', 'Protocol', 'FQDN', 'SSL', 'CVE ID', 'Vendor Reference', 'Bugtraq ID', 'CVSS Base', 'CVSS Temporal', 'Threat', 'Impact', 'Solution', 'Exploitability', 'Associated Malware', 'Results', 'PCI Vuln', 'Instance', None]



    def parse_csv(self):

        processed = 0

        with open(str(self.options.csv), newline='') as f0:
            qualys_csv = csv.DictReader(f0, fieldnames=self.fieldnames)

            with open(str(options.write), mode='w', newline='') as f1:
                output_csv = csv.DictWriter(f1, fieldnames=self.fieldnames)
                output_csv.writeheader()
                
                for row in qualys_csv:
                    processed += 1
                    if processed % 100 == 0:
                        sys.stderr.write('[+] Processed {:,} lines \r'.format(processed))

                    try:
                        severity = int(row['Severity'])
                        if not severity in self.options.severity:
                            continue
                    except (KeyError, TypeError, ValueError):
                        continue

                    if self.check_keywords(row):
                        if self.limit:
                            if self.current >= self.limit:
                                break
                        output_csv.writerow(row)
                        self.current += 1

                sys.stderr.write('\n[+] Wrote {:,} lines to {}'.format(self.current, str(self.options.write)))


    def check_keywords(self, row):

        if not self.keywords:
            return True

        for field in row.values():

            try:
                field = self.pattern.sub('', field).lower()
                #print(field)
                #sleep(.1)
            except (AttributeError, TypeError):
                continue

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

    default_filename = datetime.now().strftime('qualys_%I_%M_%S_%m_%d_%Y.csv')
    default_folder = Path.home() / 'Desktop'
    if default_folder.is_dir():
        default_filename = default_folder / default_filename
    else:
        default_filename = (Path('.') / default_filename).absolute()

    parser = argparse.ArgumentParser(description='Filter Qualys scan results from CSV')
    parser.add_argument('-o',   '--overwrite',  action='store_true',                        help='overwrite destination file if it exists')
    parser.add_argument('-w',   '--write',      type=Path,      default=default_filename,   help='output file, default = {}'.format(str(default_filename)), metavar='FILE')
    parser.add_argument('-s',   '--severity',   type=severity,  default=list(range(0,6)),   help='only output this severity - e.g. "1,3,5" or "4-5"', metavar='INT')
    parser.add_argument('-k',   '--keywords',   type=keywords,  default=[],                 help='only outputs lines matching these search term(s)', metavar='WORDS')
    parser.add_argument('-l',   '--limit',      type=int,                                   help='limit results, default = unlimited', metavar='INT')
    parser.add_argument('csv',                  type=Path,                                  help='Qualys scan CSV')

    try:
        options = parser.parse_args()
        options.csv = options.csv.absolute()
        options.write = options.write.absolute()

        if not options.csv.is_file():
            print('[!] {} doesn\'t exist'.format(str(options.csv)))
            sleep(1)
            sys.exit(1)

            if options.write.exists() and not options.overwrite:
                print('[!] {} already exists.  Consider using --overwrite')
                sleep(2)
                sys.exit(1)

        q = QualysParser(options)
        q.parse_csv()
        sys.stderr.write('\n[+] Done')

    except AssertionError as e:
        sys.stderr.write('\n[!] {}'.format(str(e)))
        sys.exit(1)
    except KeyboardInterrupt:
        sys.stderr.write('\n[!] Interrupted')
        sys.exit(1)