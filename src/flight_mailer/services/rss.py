import logging
from datetime import datetime
from itertools import chain
from time import gmtime, mktime
from typing import Any, Dict, List

import feedparser

logger = logging.getLogger(__name__)


class RssProcessor:
    def __init__(self, interval: int) -> None:
        self._interval = interval

    def parse_feeds(self, urls: List[str]) -> List[Dict[str, Any]]:
        logging.info("Parsing feeds...")
        entries = chain.from_iterable([self._get_entries_from_feed(url=u) for u in urls])
        logging.info("Sorting entries from feeds...")
        return sorted(entries, key=lambda k: k.get("timestamp"), reverse=True)

    def _get_entries_from_feed(self, url: str) -> List[Dict[str, Any]]:
        output = []
        for entry in feedparser.parse(url).entries:
            if self._within_interval(entry.published_parsed):
                entry = self._process_entry(entry)
                output.append(entry)
        return output

    def _process_entry(self, entry):
        published_time = mktime(entry.published_parsed)
        return {
            "timestamp": str(datetime.fromtimestamp(published_time)),
            "title": entry.title,
            "link": entry.link,
        }

    def _within_interval(self, published_time):
        return mktime(gmtime()) - mktime(published_time) <= self._interval
        # return mktime(gmtime()) - mktime(e.published_parsed) <= int(os.environ["INTERVAL_SEC"])
