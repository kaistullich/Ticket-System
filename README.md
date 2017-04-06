# Lightweight Ticket System

This project was the final for BUS4-92 at San Jose State University. Here are a few instructions:
 
* Have Python 3.x installed on your system: [Download](https://www.python.org/downloads/)   
 * Create a free Twilio Developer Account: [Twilio Developer Sign-up](https://www.twilio.com/try-twilio)
 * Have Git installed on your system: [Download](https://git-scm.com/downloads) and instructions for setup [here](https://git-scm.com/book/en/v2)

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