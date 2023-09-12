#!/usr/bin/env python

from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import feedparser
import html
from itertools import chain
import json
import logging
import os
import smtplib
from time import gmtime, mktime
logging.basicConfig(level=logging.INFO)


def main(event=None, context=None):

    feeds = [json.loads(line) for line in open('feeds.jsonl')]
    entries = parse_feeds(feeds)
    send_email(entries)


def send_email(entries):

    if entries:

        template = open('template.html').read()

        logging.info('Generating email message...')

        msg = MIMEMultipart('related')
        msg['From'] = os.environ['EMAIL_SENDER']
        msg['To'] = os.environ['EMAIL_RECIPIENT']
        msg['Subject'] = '{} feed update(s)'.format(len(entries))

        content = MIMEMultipart('alternative')
        content.attach(MIMEText(template.format(table=make_table(entries)), 'html'))

        msg.attach(content)


        logging.info('Setting up and connecting to SMTP server')
        s = smtplib.SMTP(host=os.environ['EMAIL_HOST'],
                         port=os.environ['EMAIL_PORT'])

        s.starttls()
        s.login(user=os.environ['EMAIL_USERNAME'],
                password=os.environ['EMAIL_PASSWORD'])

        logging.info('Sending mail...')
        s.sendmail(os.environ['EMAIL_SENDER'], os.environ['EMAIL_RECIPIENT'], msg.as_string())
        s.close()

    else:

        logging.info('No entries found within interval. No email to send')


def make_table(entries):

    logging.info('Making html table from entries...')
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

    logging.info('Parsing feeds...')
    entries = chain.from_iterable([feedparser.parse(f['link']).entries for f in feeds])
    logging.info('Sorting entries from feeds...')
    return sorted([process_entry(e) for e in entries if within_interval(e)],
                   key=lambda k: k.get('timestamp'), reverse=True)


def process_entry(e):

    return {'timestamp': str(datetime.fromtimestamp(mktime(e.published_parsed))),
            'title': e.title,
            'link': e.link}


def within_interval(e):

    return mktime(gmtime()) - mktime(e.published_parsed) <= int(os.environ['INTERVAL_SEC'])


if __name__ == '__main__':
    main()
