# automate-emails

Automate emails given a template!

Send emails to recipient(s) by using an email template of your choice while also making text substitutions.

## Set Up:
Use `pip` to install required module(s). Simply run:
```bash
pip3 install -r requirements.txt
```

*See [installing `pip`](https://pip.pypa.io/en/stable/installation/)*.

## How to Use:
`./send_email.py -h` or `./send_multiple_emails.py -h` to see command line options.

This repo stores sender's credential information and email data in untracked `.json` files -- `sender-info.json`,  `email-info.json`, and `text-replacements.json` in the `data/` folder. Templates for those files have been provided in this repo as `sender-info-template.json`, `email-info-template.json`, `text-replacements-template.json`. You can either rename these files after cloning or make new ones with the required info.

There are also helper scripts in `helpers` folder that you can run to create `sender-info.json` and `email-info.json` 
files. Make sure to run these scripts where you want to create the `json` files (i.e. inside the `data/` folder).

An example usage from `data/` folder:
```
python3 ../helpers/create-email-info-json.py -s "Test email" -f data/email-template.html
```

---

### Main Scripts

<u>`send_email.py`</u>:

Usage:
```
usage: send_email.py [-h] -r RECIPIENT_EMAIL [-l LOGGING_LEVEL]

Sends email based on the given email info and the sender's info to a recipient.

optional arguments:
  -h, --help            show this help message and exit
  -r RECIPIENT_EMAIL, --recipient_email RECIPIENT_EMAIL
                        Recipient's email address.
  -l LOGGING_LEVEL, --logging-level LOGGING_LEVEL
                        Logging level: DEBUG or INFO.
```
This script parses through the email template, performs the given text replacements, and sends an email to the 
specified recipient address. Note that logging level = `INFO` if not provided.

<u>`send_multiple_emails.py`</u>:

Usage:
```
usage: send_multiple_emails.py [-h] -r RECIPIENTS_FILE [-v VOLUNTEER] [-l LOGGING_LEVEL]

Send emails to multiple recipients based on a template.

optional arguments:
  -h, --help            show this help message and exit
  -r RECIPIENTS_FILE, --recipients_file RECIPIENTS_FILE
                        A document containing a list of emails and names of recipients. Currently supporting .csv files.
  -v VOLUNTEER, --volunteer VOLUNTEER
                        Name of person responsible for group of recipients in the data.
  -l LOGGING_LEVEL, --logging-level LOGGING_LEVEL
                        Logging level: DEBUG or INFO.
```
This script sends multiple emails to recipients who are assigned to a volunteer. This configuration/setting/structure was
born out of the need (or should I say, want) for automating emails to university alumni.

The data file (`.csv`) containing email addresses of recipients assigned to volunteers can look like:

| Volunteer assignment  | Email                  | Name |
| -------------         | -------------          | ------------- |
| Mustafa               | jondoe@u.rochester.edu | Jon |
| Mustafa               | mysteriousman@gmail.com| Mr. M |
| Somebody              | hbull@yahoo.com        | Hasbullah |

An example usage of the script can look like:
```
./send_multiple_emails.py -r data/recipients.csv -v Mustafa
```

---

### Data files

<u>`sender-info.json`</u>:

Stores the sender's name, email, and app password in order to send emails (currently through Gmail but one can edit that as required). All fields in the file are strings. See [creating an app password with Gmail](https://support.google.com/accounts/answer/185833?visit_id=638125354060183902-2645876164&p=InvalidSecondFactor&rd=1).

Sample `sender-info.json`:
```json
{
    "name": "Mr. Spira",
    "email": "spira@gmail.com",
    "app-password": "ibwopkpojojwq"
}
```

<u>`email-info.json`</u>:

Stores the email subject and body. The body is the filepath to a `.html` file containing the email text body. It is `.html` so that rich formatting can be supported. Write your email as you wish in MS Word or Google Docs and save it as a `.html` file. All fields in this file are strings.

Sample `email-info.json`:
```json
{
    "subject": "Strike out the winter blues in Philadelphia with fellow young alumni!",
    "body-template-file": "email-template.html"
}
```

<u>`text-replacements.json`</u>:

Stores the text replacements you want to perform on the email template. An example of why you'd want this is shown below.
Consider this email template:

```
Hello,

Hope you're doing well...bla...bla...bla...

Best,
[Sender Name]
[Job Title]
```

You want to replace `[Sender Name]` & `[Job Title]` with your name and job title. For this particular case, you 
can do that by adding this `text-replacements.json`:

```json
{
  "[Sender Name]": "Bahadur Ali",
  "[Job Title]": "Free soul"
}
```

**Note**: Since the email template is an html doc, you'd want the text to be replaced to be set accordingly. If the text 
to be replaced is in red color but you want the replaced text to not be of that color, you'd want to add the whole html 
style brackets -- templates converted from MS Word will work with this easily. See `data/text-replacements-template.json` 
for an example.

**Note**: If there are no text replacements to be made, an empty `text-replacements.json` will look like:

```json
{
}
```
