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
usage: filter_qualys.py [-h] [-o] [-w FILE] [-s INT] [-k WORDS] [-l INT] csv

Filter Qualys scan results from CSV

positional arguments:
  csv                   Qualys scan CSV

optional arguments:
  -h, --help            show this help message and exit
  -o, --overwrite       overwrite destination file if it exists
  -w FILE, --write FILE
                        output file, default =
                        Desktop/qualys_11_35_06_09_00_2018.csv
  -s INT, --severity INT
                        only output this severity - e.g. "1,3,5" or "4-5"
  -k WORDS, --keywords WORDS
                        only outputs lines matching this search term(s)
  -l INT, --limit INT   limit results, default = unlimited
~~~