#!/usr/bin/env python

from datetime import datetime
from email.message import EmailMessage
from email.mime.text import MIMEText
import feedparser
import html
from itertools import chain
import json
import os
import smtplib
from time import gmtime, mktime


def main():

    feeds = [json.loads(line) for line in open('feeds.jsonl')]
    entries = parse_feeds(feeds)
    send_email(entries)


def send_email(entries):

    if entries:

        template = open('template.html').read()

        msg = EmailMessage()
        msg.set_content(MIMEText(template.format(table=make_table(entries)), 'html'))
        msg['Subject'] = '{} feed update(s)'.format(len(entries))

        s = smtplib.SMTP(host=os.environ['EMAIL_HOST'],
                         port=os.environ['EMAIL_PORT'])

        s.starttls()
        s.login(user=os.environ['EMAIL_USERNAME'],
                password=os.environ['EMAIL_PASSWORD'])
        s.sendmail(os.environ['EMAIL_SENDER'], os.environ['EMAIL_RECIPIENT'], msg.as_string())
        s.close()


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

    return mktime(gmtime()) - mktime(e.published_parsed) <= int(os.environ['INTERVAL_SEC'])


if __name__ == '__main__':
    main()
