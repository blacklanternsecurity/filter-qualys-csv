# Filter Qualys Scan CSV
### Cut down on the size of Qualys' scan results by filtering based on severity, keywords, etc.  Written in Python.

### Features:
* Filter by keyword(s) or severity
* Limit number of results in output
* Cross-platform
* Outputs to user's desktop if no destination file is specified

### Example:
~~~
$ ./filter_qualys.py scan_results.csv
~~~

### Usage:
~~~
usage: filter_qualys.py [-h] [-o] [-w WRITE] [-s SEVERITY] [-k KEYWORDS]
                        [-l LIMIT]
                        csv

Filter Qualys scan results from CSV

positional arguments:
  csv                   Qualys scan CSV

optional arguments:
  -h, --help            show this help message and exit
  -o, --overwrite       overwrite destination file if it exists
  -w WRITE, --write WRITE
                        output file, default =
                        /home/bls/Desktop/qualys_13_24_06_09_00_2018.csv
  -s SEVERITY, --severity SEVERITY
                        only output this severity - e.g. "1,3,5" or "4-5"
  -k KEYWORDS, --keywords KEYWORDS
                        only outputs lines matching this search term(s)
  -l LIMIT, --limit LIMIT
                        limit results, default = unlimited
~~~