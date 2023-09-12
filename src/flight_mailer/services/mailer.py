import html
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailAdapter:
    def __init__(self, username: str, password: str, host: str, port: int, sender: str) -> None:
        self._client = self._setup_client(
            username=username, password=password, host=host, port=port
        )
        self._sender = sender

    def _setup_client(self, username: str, password: str, host: str, port: str):
        logging.info("Setting up and connecting to SMTP server")
        s = smtplib.SMTP(host=host, port=port)
        s.starttls()
        s.login(user=username, password=password)
        return s

    def close(self) -> None:
        self._client.close()

    def send_email(self, recipient: str, subject: str, payload: str) -> None:
        logging.info("Generating email message...")

        msg = MIMEMultipart("related")
        msg["From"] = self._sender
        msg["To"] = recipient
        msg["Subject"] = subject

        content = MIMEMultipart("alternative")
        content.attach(MIMEText(payload, "html"))
        msg.attach(content)

        logging.info("Sending mail...")
        self._client.sendmail(self._sender, recipient, msg.as_string())

    def _make_payload(self, entries) -> str:
        with open("template.html") as fp:
            template = fp.read()
            return template.format(table=self._make_table(entries))

    @staticmethod
    def _make_table(entries) -> str:
        logging.info("Making html table from entries...")
        output = ""

        for entry in entries:
            output += "<tr>"
            if entries.index(entry) == 0:
                for key in entry.keys():
                    output += f"<th>{html.escape(key.capitalize())}</th>"
                output += "</tr><tr>"
            for key, value in entry.items():
                value = html.escape(value)
                if key == "link":
                    output += f"<td><a target=_blank href={value}>here</a></td>"
                else:
                    output += f"<td>{value}</td>"
            output += "</tr>"

        return output
