import os
from functools import cached_property


class Configuration:
    @cached_property
    def email_sender(self) -> str:
        return os.environ["EMAIL_SENDER"]

    @cached_property
    def email_recipient(self) -> str:
        return os.environ["EMAIL_RECIPIENT"]

    @cached_property
    def email_host(self) -> str:
        return os.environ["EMAIL_HOST"]

    @cached_property
    def email_port(self) -> str:
        return os.environ["EMAIL_PORT"]

    @cached_property
    def email_username(self) -> str:
        return os.environ["EMAIL_USERNAME"]

    @cached_property
    def email_password(self) -> str:
        return os.environ["EMAIL_PASSWORD"]

    @cached_property
    def interval_seconds(self) -> int:
        return 86400
        # return int(os.environ["INTERVAL_SEC"])
