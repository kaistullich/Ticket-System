# Lightweight Ticket System

This project was the final for BUS4-92 at San Jose State University. Here are a few instructions:
 
* Have Python 3.x installed on your system: [Download](https://www.python.org/downloads/)   
 * Create a free Twilio Developer Account: [Twilio Developer Sign-up](https://www.twilio.com/try-twilio)
 * Have Git installed on your system: [Download](https://git-scm.com/downloads) and instructions for setup [Here](https://git-scm.com/book/en/v2)
 * Sign-up for a free Gmail email account if you do not already have one: [Gmail Sign-up](https://accounts.google.com/SignUp?hl=en-GB)

After completing the steps above clone the directory wherever you would like to place it

```
$ git clone https://github.com/kaistullich/Ticket-System.git
$ cd Ticket-System
```

Then install all dependencies:

`$ pip3 install -r requirements.txt`

Now, open up a `Ticket-System` in a text editor. Create a new file called `config.json`. The folder structure will look like this:

```
Ticket-System\
    src\
        static\
        templates\
    __init__.py
    decorators.py
    models.py
    views.py
    config.json
.gitignore
README.md
run.py
ticket_system.sqlite

```

The order of some files _MAY_ be different, but all file names **should** be the same.

Open the `config.json` file you just created, and paste in the following JSON:

```
{
  "DATABASE_FILE": "ticket_system.sqlite",
  "SQLALCHEMY_DATABASE_URI": "sqlite://///",
  "SQLALCHEMY_ECHO": true,
  "SQLALCHEMY_TRACK_MODIFICATIONS": true,
  "MAIL_SERVER": "smtp.gmail.com",
  "MAIL_PORT": "465",
  "MAIL_USERNAME": "",
  "MAIL_PASSWORD": "",
  "MAIL_USE_TLS": false,
  "MAIL_USE_SSL": true,
  "account_sid": "",
  "auth_token": "",
  "from_": ""
}
```