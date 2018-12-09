#!/usr/bin/env python

import feedparser
from datetime import datetime
from time import time, mktime
import json
import html
from itertools import chain

INTERVAL_SEC = 21600 # 6 hours

def main():
    feeds = [json.loads(line) for line in open('feeds.jsonl')]
    entries = parse_feeds(feeds)
    template = open('template.html').read()
    open('email.html', 'w').write(template.format(table=make_table(entries)))
   # with open('entries.jsonl', 'w') as f:
   #     for e in entries:
   #         f.write(json.dumps(e) + '\n')


def make_table(entries):
    output = ''

    for e in entries:
        output += '<tr>'
        if entries.index(e) == 0:
            output += ''.join('<th>{}</th>'.format(html.escape(k.capitalize())) for k in e.keys()) + '</tr><tr>'
        for k, v in e.items():
            v = html.escape(v)
            if k == 'link':
               output += '<td><a target=_blank href={}>here</a></td>'.format(v)
            else:
                output += '<td>{}</td>'.format(v)
        output += '</tr>'

    return output


def parse_feeds(feeds):
    entries = chain.from_iterable([feedparser.parse(f['link']).entries for f in feeds])
    return sorted([process_entry(e) for e in entries
                   if within_interval(e)], key=lambda k: k.get('timestamp'), reverse=True)


def process_entry(e):
    return {'timestamp': str(datetime.fromtimestamp(mktime(e.published_parsed))),
            'title': e.title,
            'link': e.link}



def within_interval(e):
    return time() - mktime(e.published_parsed) <= INTERVAL_SEC

if __name__ == '__main__':
    main()
