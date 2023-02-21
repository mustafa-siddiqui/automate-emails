import argparse
import csv
import json
import re

#
# Constants
#

# currently set to work with gmail
SMTP_SERVER_DOMAIN_NAME = "smtp.gmail.com"
SMTP_SERVER_PORT = 587

# to validate email format
EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

# sender info json file path respective to this file
SENDER_INFO_JSON_FILE = "sender-info.json"

# email template html file path respective to this file
EMAIL_TEMPLATE_FILE = "email-template.html"

# text to find in template and replace with sender info
REPLACE_WITH_NAME_MATCHER = "[<span style='color:red'>Sender name</span>]"
REPLACE_WITH_CLASS_YEAR_MATCHER = "[<span style='color:red'>Year</span>]"

#
# Classes
#

class SenderInfo:
    """Class to store validated sender info."""

    def __init__(self, sender_info_json_obj) -> None:
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
    """Reads sender info json file, validates email address, and returns a dictionary of the info.
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

def parse_email_template(email_template: str, sender_info: SenderInfo) -> str:
    """Opens and processes email template from MS Word file format to extract text and return 
    a string representation containing the sender's name and class year."""

    file = open(email_template, "r")
    template_html_text = file.read()
    file.close()

    template_modified = template_html_text.replace(REPLACE_WITH_NAME_MATCHER, sender_info.name)
    email_body_html_text = template_modified.replace(REPLACE_WITH_CLASS_YEAR_MATCHER, sender_info.class_year)

    return email_body_html_text


def substitute_names_and_create_individual_files(
    user_details: dict, template: str
) -> bool:
    """Goes through the user info dictionary and creates individual text files for each user with the
    substituted text. Returns true if no errors encountered, false if otherwise.
    """


def send_email(sender_email: str, user_details: SenderInfo, email_text: str) -> None:
    """Send email to one recipient given the sender info and email body in html."""

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
    
    print(parse_email_template(EMAIL_TEMPLATE_FILE, get_sender_info(SENDER_INFO_JSON_FILE)))


if __name__ == "__main__":
    main()
