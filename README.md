# automate-emails

Automate emails given a template!

This current implementation is written for a specific case of sending emails to university alumni but with a few changes can be used by anyone as they wish. Currently, the email template has two fields -- [Sender name] and [Year] -- that the script replaces with the sender's name and class year.

# Set Up:
Use `pip` to install required module(s). Simply run:
```bash
pip3 install -r requirements.txt
```

*See [installing `pip`](https://pip.pypa.io/en/stable/installation/)*.

## How to Use:
`python3 send_email.py -h` or `python3 send_multiple_emails.py -h` to see command line options.

This repo stores sender's credential information and email data in untracked `.json` files -- `sender-info.json` and `email-info.json`. Templates for those files have been provided in this repo as `sender-info-template.json` and `email-info-template.json`. You can either rename these files after cloning or make new ones with the required info.

`send_email.py`:

Usage:
```bash
usage: send_email.py [-h] -r RECIPIENT_EMAIL

Sends email based on the given email info and the sender's info to a recipient.

optional arguments:
  -h, --help            show this help message and exit
  -r RECIPIENT_EMAIL, --recipient_email RECIPIENT_EMAIL
                        Recipient's email address.
```
This script parses through the email template and sends an email to the specified recipient address.

`send_multiple_emails.py`:

Usage:
```bash
usage: send_multiple_emails.py [-h] -r RECIPIENTS_FILE [-v VOLUNTEER]

Send emails to multiple recipients based on a template.

optional arguments:
  -h, --help            show this help message and exit
  -r RECIPIENTS_FILE, --recipients_file RECIPIENTS_FILE
                        A document containing a list of emails and names of recipients. Currently supporting .csv files.
  -v VOLUNTEER, --volunteer VOLUNTEER
                        Name of person responsible for group of recipients in the data.
```
This script sends multiple emails to recipients who are assigned to one volunteer.

The data file (`.csv`) containing email addresses of recipients assigned to volunteers can look like:

| Volunteer assignment  | Email                  | Name |
| -------------         | -------------          | ------------- |
| Mustafa               | jondoe@u.rochester.edu | Jon |
| Somebody              | hbull@yahoo.com        | Hasbullah |

`sender-info.json`:

Stores the sender's name, email, class year, and app password in order to send emails (currently through Gmail but one can edit that as required). All fields in the file are strings. See [creating an app password with Gmail](https://support.google.com/accounts/answer/185833?visit_id=638125354060183902-2645876164&p=InvalidSecondFactor&rd=1).

Sample `sender-info.json`:
```json
{
    "name": "Mr. Spira",
    "class-year": "2022",
    "email": "spira@gmail.com",
    "app-password": "ibwopkpojojwq"
}
```

`email-info.json`:

Stores the email subject and body. The body is the filepath to a `.html` file containing the email text body. It is `.html` so that rich formatting can be supported. Write your email as you wish in MS Word or Google Docs and save it as a `.html` file. All fields in this file are strings.

Sample `email-info.json`:
```json
{
    "subject": "Strike out the winter blues in Philadelphia with fellow young alumni!",
    "body-template-file": "email-template.html"
}
```


## Next Steps:
- [x] Make `requirements.txt` for module dependencies
- [x] Add logger for logging
- [x] Create helper scripts to generate `.json` files
- [ ] Make text replacements generic/editable by the user
