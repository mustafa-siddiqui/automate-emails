import argparse
import json


def main():
    parser = argparse.ArgumentParser(
        description="""Helper script to generate email-info.json file."""
    )

    parser.add_argument(
        "-s",
        "--subject",
        help="""Subject text of the email.""",
        type=str,
        required=True,
    )

    parser.add_argument(
        "-f",
        "--template_file_path",
        help="""File path to the email body text (.html) template.""",
        type=str,
        required=True,
    )

    args = parser.parse_args()

    file_content = json.dumps(
        {"subject": args.subject, "body-template-file": args.template_file_path}
    )

    file = open("email-info.json", "w")
    file.write(file_content)
    file.close()


if __name__ == "__main__":
    main()
