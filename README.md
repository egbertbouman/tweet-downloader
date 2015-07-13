# tweet-downloader
Simple script for downloading tweets without using the Twitter API. The output is in JSON format.

### Dependencies
* Python 2.7+
* requests
* beautifulsoup4 

The python packages can be installed with

    pip install beautifulsoup4
    pip install requests


### Usage
```
usage: tweet_downloader.py [--help] [--search SEARCH] [--profile PROFILE]
                           [--output OUTPUT]

Download tweets without using the Twitter API

optional arguments:
  --help, -h            Show this help message and exit
  --search SEARCH, -s SEARCH
                        Search query (e.g., "\"london news\" since:2012-04-01 until:2012-07-31)"
  --profile PROFILE, -p PROFILE
                        Profile query
  --output OUTPUT, -o OUTPUT
                        Output filename
```
