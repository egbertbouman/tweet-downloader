import sys
import time
import json
import requests
import argparse
import urllib

from tweet_parser import parse_search_results

TWITTER_PROFILE_URL = 'https://twitter.com/{term}'
TWITTER_PROFILE_MORE_URL = 'https://twitter.com/i/profiles/show/{term}/timeline?include_available_features=1&include_entities=1&max_position={max_position}'
TWITTER_SEARCH_URL = 'https://twitter.com/search?q={term}&src=typd'
TWITTER_SEARCH_MORE_URL = 'https://twitter.com/i/search/timeline?q={term}&src=typd&vertical=default&include_available_features=1&include_entities=1&max_position={max_position}'


def find_value(html, key):
    pos_begin = html.find(key) + len(key) + 2
    pos_end = html.find('"', pos_begin)
    return html[pos_begin: pos_end]

def download_tweets(search=None, profile=None, sleep=1):
    assert search or profile

    tweets = 0
    term = (search or profile)
    url = TWITTER_SEARCH_URL if search else TWITTER_PROFILE_URL
    url_more = TWITTER_SEARCH_MORE_URL if search else TWITTER_PROFILE_MORE_URL

    response = requests.get(url.format(term=term)).text
    max_position = find_value(response, 'data-max-position')
    min_position = find_value(response, 'data-min-position')

    for tweet in parse_search_results(response.encode('utf8')):
        yield tweet
        tweets += 1

    has_more_items = True
    while has_more_items:
        response = requests.get(url_more.format(term=term, max_position=min_position)).text
        response_dict = json.loads(response)
        min_position = response_dict['min_position']
        has_more_items = response_dict['has_more_items'] if profile else False

        for tweet in parse_search_results(response_dict['items_html'].encode('utf8')):
            yield tweet
            tweets += 1

            if search:
                has_more_items = True

        time.sleep(sleep)


def main(argv):
    parser = argparse.ArgumentParser(add_help=False, description=('Download tweets without using the Twitter API'))
    parser.add_argument('--help', '-h', action='help', default=argparse.SUPPRESS, help='Show this help message and exit')
    parser.add_argument('--search', '-s', type=str, help='Search query (e.g., "\\"london news\\" since:2012-04-01 until:2012-07-31)"')
    parser.add_argument('--profile', '-p', help='Profile query')
    parser.add_argument('--output', '-o', help='Output filename')

    try:
        args = parser.parse_args(argv)

        search = args.search
        profile = args.profile
        output = args.output

        if bool(search) == bool(profile):
            parser.print_usage()
            raise ValueError('you need to use either the search or the profile option')

        if not output:
            parser.print_usage()
            raise ValueError('you need to specify an output filename')

        print 'Downloading', (search or profile)

        count = 0
        with open(output, 'wb') as fp:
            for tweet in download_tweets(search=search, profile=profile):
                print >> fp, json.dumps(tweet)
                count += 1
                sys.stdout.write('Fetched %d tweet(s)\r' % count)
                sys.stdout.flush()
        print 'Done!'


    except Exception, e:
        print 'Error:', str(e)
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
