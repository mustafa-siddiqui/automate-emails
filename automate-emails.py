import argparse
import csv
import json
import re
import smtplib

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

def validate_email(email: str) -> bool:
    """Performs a basic check to see if the email provided is in a valid format. Does not 
    validate if the email address actually exists or not."""

    if not EMAIL_REGEX.match(email):
        return False

    return True

def get_sender_info(sender_info_file: str) -> SenderInfo:
    """Reads sender info json file, validates email address, and returns a SenderInfo object.
    Returns None if email not valid."""

    file = open(sender_info_file, "r")
    sender_info = json.load(file)
    file.close()

    if not validate_email(sender_info["email"]):
        return None

    return SenderInfo(sender_info)

def read_data_file(data_file: str) -> dict:
    """Parses through .csv data file and creates a dictionary of recipients' names with their
    email addresses."""

def parse_email_template(template_html_text: str, sender_info: SenderInfo) -> str:
    """Parses through the email's body in HTML format and returns a string representation 
    containing the sender's name and class year."""

    template_modified = template_html_text.replace(REPLACE_WITH_NAME_MATCHER, sender_info.name)
    email_body_html_text = template_modified.replace(REPLACE_WITH_CLASS_YEAR_MATCHER, sender_info.class_year)

    return email_body_html_text

def get_email_info(email_info_file: str, sender_info: SenderInfo) -> EmailInfo:
    """Reads email info json file and returns a EmailInfo object with matchers replaced with sender's info."""

    file = open(email_info_file, "r")
    email_info = json.load(file)
    file.close()

    email_info_obj = EmailInfo(email_info)
    email_info_obj.body = parse_email_template(email_info_obj.body, sender_info)

    return email_info_obj

def connect_to_smtp_server(sender_info: SenderInfo) -> smtplib.SMTP:
    """Connects to the SMTP server given the server domain name, port info, and sender login details.
    Returns an SMTP object if successful, None if not. """

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
        print("Error: cannot login to SMPT server. Check your login credentials. {" + str(error) + "}")
        return None

    return smtp_server_obj

def disconnect_from_smtp_server(smtp_server_obj: smtplib.SMTP) -> None:
    """Disconnects from the SMTP server."""

    smtp_server_obj.quit()


def send_email(smtp_server_obj: smtplib.SMTP, sender_email: str, user_details: SenderInfo, email_text: str) -> None:
    """Send email to one recipient given the sender info and email body in html."""

    message = MIMEMultipart("alternative")

    message["Subject"] = "Test Message"
    message["From"] = "mustafa.eins@gmail.com"
    message["To"] = "msiddiq7@u.rochester.edu"

#
# MAIN
#

def main():
    parser = argparse.ArgumentParser(
        description="""Parses through email data of recipients and sends emails based on provided 
        email template."""
    )

    parser.add_argument(
        "--email_template",
        help="""A text file containing the email template.""",
        type=str,
        required=True,
    )

    parser.add_argument(
        "--data_file",
        help="""A .csv file containing receipients' name and email data.""",
        type=str,
        required=True,
    )

    parser.parse_args()
    
    # test code
    if get_sender_info(SENDER_INFO_JSON_FILE) is not None:
        print("Success")
    else:
        print("You suck.")
    
    if get_email_info(EMAIL_INFO_JSON_FILE, get_sender_info(SENDER_INFO_JSON_FILE)) is not None:
        print("Success x2")
        print(get_email_info(EMAIL_INFO_JSON_FILE, get_sender_info(SENDER_INFO_JSON_FILE)).subject)
    else:
        print("You suck. x2")


if __name__ == "__main__":
    main()
