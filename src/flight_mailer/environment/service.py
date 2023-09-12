from functools import cached_property

from flight_mailer.environment.configuration import Configuration
from flight_mailer.services.mailer import EmailAdapter
from flight_mailer.services.rss import RssProcessor


class ServiceProvider:
    @cached_property
    def config(self) -> Configuration:
        return Configuration()

    @cached_property
    def rss_processor(self) -> RssProcessor:
        return RssProcessor(interval=self.config.interval_seconds)

    @cached_property
    def email_adapter(self) -> EmailAdapter:
        return EmailAdapter(
            username=self.config.email_username,
            password=self.config.email_password,
            host=self.config.email_host,
            port=self.config.email_port,
            sender=self.config.email_sender,
        )
