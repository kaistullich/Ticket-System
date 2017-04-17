# Lightweight Ticket System

****!!!! NOTE: _Please be aware that the README is not fully updated, and some instructions are missing. With the
information provided you will NOT be able to run the system, unless you have a intermediate background with
Python and/or Twilio and/or Flask and are willing to work out all the errors that will occur. I hope to update the
README to full completion in the near future. Thank you for your understanding._ !!!!****


**~~ LAST UPDATE: 04/17/2017 ~~**


***
This project was the final for the BUS4-110A course at San Jose State University. Here are a few instructions if you would
like to test the system out:
 
* Have Python 3.x installed on your system: [Download](https://www.python.org/downloads/)   
 * Create a free Twilio Developer Account: [Twilio Developer Sign-up](https://www.twilio.com/try-twilio)
 * Have Git installed on your system: [Download](https://git-scm.com/downloads) and instructions for setup [here](https://www.atlassian.com/git/tutorials/install-git#windows)
    * _Follow the instructions for your given Operating System_
 * Sign-up for a free Gmail email account if you do not already have one: [Gmail Sign-up](https://accounts.google.com/SignUp?hl=en-GB)
 * Head to [ngrok](https://ngrok.com/download) and download the free HTTPS relayer. Follow the simple setup provided by `ngrok`.
    * _Make sure to download and unzip `ngrok` in a folder that you are able to access (i.e. Downloads, Documents etc.)_


***
## SETUP
#### Part 1:
After completing the steps above clone the directory wherever you would like to place it

```
$ git clone https://github.com/kaistullich/Ticket-System.git
$ cd Ticket-System
```

Then install all dependencies:

`$ pip3 install -r requirements.txt` (MacOSX)

`$ pip install -r requirements.txt` (Windows)


Now, open up `Ticket-System` in a text editor. Create a new file called `config.json` inside the `src` folder. 
The folder structure will look like this:

```
Ticket-System\
    src\
        static\
        templates\
    __init__.py
    all_notifications.py
    config.json
    decorators.py
    models.py
    views.py
.gitignore
api_check.py
config_instructions.txt
README.md
requirements.txt
run.py

```

***


#### Part 2:
Open the `config.json` file you just created, and paste in the following JSON:

```json
{
  "DATABASE_FILE": "ticket_system.sqlite",
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
  "from_": "",
  "dept_num": "",
  "reminder": "",
  "ticket_creation": "",
  "api_url": ""
}
```

Follow the instructions inside of the `config_instructions.txt` file to fill in the blank values.

### Part 3:
Create the SQLite DB. To do this, open your _Terminal_ or _CMD_ and navigate to the top level of the folder 
structure. From there type in `python3` (MaxOSx) or `python` (Windows) and execute the following commands:

```
$ ~/Ticket-System python3

Python 3.5.2 (v3.5.2:4def2a2901a5, Jun 26 2016, 10:47:25) 
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.

>>> from src.models import db
>>> db.create_all()
```

This will spit out a bunch of information regarding the creation of the Database and all of the tables inside of
it.
***

## Launch App

We are now ready to start-up the system. Head into your Terminal or CMD.
Enter the following command:

`$ pip3 run.py` (MacOSX)

`$ pip run.py` (Windows)

By running this command you can open up any web browser and navigate to the HTTPS Forwarding that `ngrok` displays
`(i.e. https://bcd848e3.ngrok.io)`. 

Likewise you could also just go to `localhost:5000` or `127.0.0.1:5000`. But I would recommend using the `ngrok` url to 
make sure that everything is working properly. 