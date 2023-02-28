#!/usr/bin/env python3

import argparse
import logging
import send_email
import csv


def _get_list_of_dict(recipients_file: str) -> list:
    """Parses the given .csv file and returns a list of dictionaries containing recipient data."""

    file = open(recipients_file, mode="r", encoding="utf-8-sig")
    recipients = csv.DictReader(file)

    recipients_as_array = []
    for row in recipients:
        recipients_as_array.append(row)

    file.close()

    return recipients_as_array


def main():
    parser = argparse.ArgumentParser(
        description="""Send emails to multiple recipients based on a template."""
    )

    parser.add_argument(
        "-r",
        "--recipients_file",
        help="A document containing a list of emails and names of recipients. Currently supporting .csv files.",
        type=str,
        required=True,
    )

    parser.add_argument(
        "-v",
        "--volunteer",
        help="Name of person responsible for group of recipients in the data.",
        type=str,
        required=False,
    )

    parser.add_argument(
        "-l",
        "--logging-level",
        help="""Logging level: DEBUG or INFO.""",
        type=str,
        required=False,
    )

    args = parser.parse_args(args)

    logging_level = logging.INFO
    if args.logging_level == "DEBUG":
        logging_level = logging.DEBUG
    elif args.logging_level == "INFO":
        pass
    elif args.logging_level is None:
        pass
    else:
        print("Error: Incorrect logging level. Valid options are INFO or DEBUG.")
        return

    logging.basicConfig(
        level=logging_level,
        format="[%(asctime)s]: [%(levelname)s]: %(message)s",
        datefmt="%Y-%m-%d - %H:%M:%S",
    )

    recipients = _get_list_of_dict(args.recipients_file)
    if len(recipients) == 0:
        logging.error("No recipients found after reading .csv file.")
        return

    # Send emails to recipients assigned to volunteer if specified
    # If not, send to all one by one
    for recipient in recipients:
        recipient_email = recipient["Email"]
        if args.volunteer is not None:
            if recipient["Volunteer assignment"] == args.volunteer:
                logging.info(
                    f"Sending email to {recipient['Name']} @ {recipient['Email']}..."
                )
                send_email.main(["-r", recipient_email])
            else:
                pass
        else:
            logging.info(
                f"Sending email to {recipient['Name']} @ {recipient['Email']}..."
            )
            send_email.main(["-r", recipient_email])


if __name__ == "__main__":
    main()
