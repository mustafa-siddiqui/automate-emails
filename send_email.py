import argparse
import csv
import json
import re
import smtplib
import sys

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#
# Constants
#

# Simple Mail Transfer Protocol (SMTP) server details
# currently set to work with gmail
SMTP_SERVER_DOMAIN_NAME = "smtp.gmail.com"
SMTP_SERVER_PORT = 587

# to validate email format
EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

# sender info json file path respective to this file
SENDER_INFO_JSON_FILE = "sender-info.json"

# email info json file path respective to this file
EMAIL_INFO_JSON_FILE = "email-info.json"

# text to find in template and replace with sender info
REPLACE_WITH_NAME_MATCHER = "[<span style='color:red'>Sender name</span>]"
REPLACE_WITH_CLASS_YEAR_MATCHER = "[<span style='color:red'>Year</span>]"

#
# Classes
#


class EmailInfo:
    """Class to store email subject and body text."""

    def __init__(self, email_info_json_obj: dict) -> None:
        """Class constructor.
        subject: str
        body: str"""

        self.subject = email_info_json_obj["subject"]
        filepath = email_info_json_obj["body-template-file"]
        file = open(filepath, "r")
        self.body = file.read()
        file.close()

    def __str__(self) -> str:
        """Returns a string representation of the object."""

        str_repr = ""
        str_repr += "{Subject: " + self.subject + ", "
        str_repr += "Body: " + self.body + "}"

        return str_repr


class SenderInfo:
    """Class to store validated sender info."""

    def __init__(self, sender_info_json_obj: dict) -> None:
        """Class constructor.
        name: str
        class_year: str
        email: str
        app_password: str
        """

        self.name = sender_info_json_obj["name"]
        self.class_year = sender_info_json_obj["class-year"]
        self.email = sender_info_json_obj["email"]
        self.app_password = sender_info_json_obj["app-password"]

    def __str__(self) -> str:
        """Returns a string representation of the object excluding the app password."""

        str_repr = ""
        str_repr += "{Name: " + self.name + ", "
        str_repr += "Class Year: " + self.class_year + ", "
        str_repr += "Email: " + self.email + "}"

        return str_repr


#
# Function Definitions
#


def _validate_email(email: str) -> bool:
    """Helper function that performs a basic check to see if the email provided is in a valid
    format. Does not validate if the email address actually exists or not."""

    if not EMAIL_REGEX.match(email):
        return False

    return True


def get_sender_info(sender_info_file: str) -> SenderInfo:
    """Reads sender info json file, validates email address, and returns a SenderInfo object.
    Returns None if email not valid."""

    file = open(sender_info_file, "r")
    sender_info = json.load(file)
    file.close()

    if not _validate_email(sender_info["email"]):
        return None

    return SenderInfo(sender_info)


def read_data_file(data_file: str) -> dict:
    """Parses through .csv data file and creates a dictionary of recipients' names with their
    email addresses."""


def _parse_email_template(template_html_text: str, sender_info: SenderInfo) -> str:
    """Helper function that parses through the email's body in HTML format and returns a string representation
    containing the sender's name and class year."""

    template_modified = template_html_text.replace(
        REPLACE_WITH_NAME_MATCHER, sender_info.name
    )
    email_body_html_text = template_modified.replace(
        REPLACE_WITH_CLASS_YEAR_MATCHER, sender_info.class_year
    )

    return email_body_html_text


def get_email_info(email_info_file: str, sender_info: SenderInfo) -> EmailInfo:
    """Reads email info json file and returns a EmailInfo object with matchers replaced with sender's info."""

    file = open(email_info_file, "r")
    email_info = json.load(file)
    file.close()

    email_info_obj = EmailInfo(email_info)
    email_info_obj.body = _parse_email_template(email_info_obj.body, sender_info)

    return email_info_obj


def connect_to_smtp_server(sender_info: SenderInfo) -> smtplib.SMTP:
    """Connects to the SMTP server given the server domain name, port info, and sender login details.
    Returns an SMTP object if successful, None if not."""

    # connect to the server
    try:
        smtp_server_obj = smtplib.SMTP(SMTP_SERVER_DOMAIN_NAME, SMTP_SERVER_PORT)
    except OSError as error:
        print("Error: Cannot connect to SMTP server. {" + str(error) + "}")
        return None

    smtp_server_obj.starttls()

    # login to service provider
    try:
        smtp_server_obj.login(sender_info.email, sender_info.app_password)
    except smtplib.SMTPAuthenticationError as error:
        print(
            "Error: cannot login to SMPT server. Check your login credentials. {"
            + str(error)
            + "}"
        )
        return None

    return smtp_server_obj


def disconnect_from_smtp_server(smtp_server_obj: smtplib.SMTP) -> None:
    """Disconnects from the SMTP server."""

    smtp_server_obj.quit()


def send_email(
    smtp_server_obj: smtplib.SMTP,
    sender_info: SenderInfo,
    email_info: EmailInfo,
    recipient_email: str,
) -> None:
    """Send email to one recipient given the sender info and email info.
    Assumes the recipient email is validated."""

    message = MIMEMultipart("alternative")

    message["Subject"] = email_info.subject
    message["From"] = sender_info.email
    message["To"] = recipient_email

    email_body_text = MIMEText(email_info.body, "html")
    message.attach(email_body_text)

    smtp_server_obj.sendmail(sender_info.email, recipient_email, message.as_string())


#
# Main
#


def main(args):
    parser = argparse.ArgumentParser(
        description="""Sends email based on the given email info and the sender's info to a recipient."""
    )

    parser.add_argument(
        "-r",
        "--recipient_email",
        help="""Recipient's email address.""",
        type=str,
        required=True,
    )

    args = parser.parse_args(args)

    if not _validate_email(args.recipient_email):
        print("Error: Invalid email address for recipient.")
        exit()

    recipient_email = args.recipient_email

    sender_info = get_sender_info(SENDER_INFO_JSON_FILE)
    if sender_info is None:
        print("Error: sender email not valid. Check sender-info.json")
        exit()

    email_info = get_email_info(EMAIL_INFO_JSON_FILE, sender_info)

    smtp_server = connect_to_smtp_server(sender_info)
    if smtp_server is None:
        print("Error: cannot connect to SMTP server.")
        exit()

    send_email(smtp_server, sender_info, email_info, recipient_email)

    disconnect_from_smtp_server(smtp_server)


if __name__ == "__main__":
    main(sys.argv[1:])
