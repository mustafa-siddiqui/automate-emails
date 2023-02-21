import argparse
import csv


def read_data_file(data_file: str) -> dict:
    """Parses through .csv data file and creates a dictionary of recipients' names with their
    email addresses."""


def read_email_template(email_template: str) -> None:
    """Opens and processes email template from MS Word file format to extract text and create
    a text file."""


def substitute_names_and_create_individual_files(
    user_details: dict, template: str
) -> bool:
    """Goes through the user info dictionary and creates individual text files for each user with the
    substituted text. Returns true if no errors encountered, false if otherwise.
    """


def send_emails(sender_email: str, user_details: dict, template: str):
    """To-Do: Instead of creating individual text files of substituted text, substitute text in place,
    and send emails directly."""


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
