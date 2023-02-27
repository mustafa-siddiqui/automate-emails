import argparse
import json


def main():
    parser = argparse.ArgumentParser(
        description="""Helper script to generate sender-info.json file."""
    )

    parser.add_argument(
        "-n",
        "--name",
        help="""Name of the sender.""",
        type=str,
        required=True,
    )

    parser.add_argument(
        "-c",
        "--class_year",
        help="""Class year of the sender.""",
        type=str,
        required=True,
    )

    parser.add_argument(
        "-e",
        "--email",
        help="""Email of the sender.""",
        type=str,
        required=True,
    )

    parser.add_argument(
        "-p",
        "--app_password",
        help="""App password of the sender.""",
        type=str,
        required=True,
    )

    args = parser.parse_args()

    file_content = json.dumps(
        {
            "name": args.name,
            "class-year": args.class_year,
            "email": args.email,
            "app-password": args.app_password,
        }
    )

    file = open("sender-info.json", "w")
    file.write(file_content)
    file.close()


if __name__ == "__main__":
    main()
