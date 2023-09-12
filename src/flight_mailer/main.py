import json
import logging

from aws_lambda_context import LambdaContext, LambdaDict

from flight_mailer.environment.service import ServiceProvider
from flight_mailer.services.mailer import EmailAdapter

logging.basicConfig(level=logging.INFO)


def main(event: LambdaDict = None, context: LambdaContext = None) -> None:
    service_provider = ServiceProvider()
    rss_processor = service_provider.rss_processor

    feeds = [json.loads(line) for line in open("feeds.jsonl")]
    urls = [feed["link"] for feed in feeds]
    entries = rss_processor.parse_feeds(urls=urls)

    if entries:
        table = EmailAdapter._make_table(entries)
        print(table)
        pass
        # send_email(entries)
    else:
        logging.info("No entries found within interval. No email to send")


if __name__ == "__main__":
    main()
