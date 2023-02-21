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

#
# Function Definitions
#

def validate_email(email: str) -> bool:
    """Performs a basic check to see if the email provided is in a valid format. Does not 
    validate if the email address actually exists or not."""

    if not EMAIL_REGEX.match(email):
        return False

    return True

def get_sender_info(sender_info_file: str) -> dict:
    """Reads sender-info.json, validates email address, and returns a dictionary of the info."""

    file = open("sender-info.json", "r")
    sender_info = json.load(file)
    file.close()

    return sender_info

def read_data_file(data_file: str) -> dict:
    """Parses through .csv data file and creates a dictionary of recipients' names with their
    email addresses."""

def read_email_template(email_template: str) -> str:
    """Opens and processes email template from MS Word file format to extract text and return 
    a string representation."""

    file = open(email_template, "r")
    template_html_text = file.read()
    file.close()

    return template_html_text


def substitute_names_and_create_individual_files(
    user_details: dict, template: str
) -> bool:
    """Goes through the user info dictionary and creates individual text files for each user with the
    substituted text. Returns true if no errors encountered, false if otherwise.
    """


def send_emails(sender_email: str, user_details: dict, template: str):
    """To-Do: Instead of creating individual text files of substituted text, substitute text in place,
    and send emails directly."""

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


if __name__ == "__main__":
    main()
