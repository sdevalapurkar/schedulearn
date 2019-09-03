# Schedulearn

A web app that tutors and students can use to schedule lessons efficiently with each other.

The service is available for free use at `https://www.schedulearn.com`

![Homepage](/img/homepage.png)

![Schedule](/img/schedule.png)

## Important Note

In order to make our web app work, you need to add important information by creating a python file called local_settings.py in the following directory: schedule_lessons/schedule_lessons/local_settings.py and copy the following code. After pasting the code in, fill in the blanks to make our web app work.

````
EMAIL_HOST = # A string of your email host e.g. 'smtp.zoho.com'
SCHEDULER_NOTIFY_EMAIL = # A string of your email address that you use to notify people when a lesson has been scheduled
VERIFY_USER_EMAIL = # A string of your email address that you use to verify users when a user signs up.
FORGET_PASSWORD_EMAIL = # A string of your email address that you use to email users who forget their password.
EMAIL_HOST_PASSWORD = # The password to your emails
EMAIL_PORT = # An integer that's your email port e.g. 587
EMAIL_USE_TLS = # a boolean value which says whether your email uses TLS or not
````

## Running the Application Locally

### NOTE: This project is using python 3.6.5 and Django 2.0.6

a. Using your terminal or command prompt, navigate to your workspace directory.

b. You need to clone our repo on the terminal. You can do this by the following command:
````
bash
#!/bin/bash
$ git clone https://github.com/sdevalapurkar/schedulearn.git
````

c. Assuming you have python3.6.5 installed, you can install our dependencies using pip.

#### Side note: We recommend you install these dependencies in a virtual environment

In order to do this in a virtual env, start your virtual environment and follow the following steps:

a. Start the virtual environment

```bash
#!/bin/bash
$ virtualenv -p python3.6.5 schedulearn_venv
```

b. Activate the virtual environment

```bash
#!/bin/bash
$ source schedulearn_venv/bin/activate
```

c. Navigate inside our repo:

```bash
#!/bin/bash
  $ cd schedulearn
```

d. Download our dependencies:

```bash
#!/bin/bash
  $ pip3 install -r requirements.txt
```

e. Navigate inside our django project:

```bash
#!/bin/bash
$ cd schedule_lessons
```

f. Now you want to migrate our database.

```bash
#!/bin/bash
$ python3 manage.py migrate
```

g. Run the application

```bash
#!/bin/bash
$ python3 manage.py runserver
```

##### After running that command, you should get the following output

```bash
#!/bin/bash
Performing system checks...

System check identified no issues (0 silenced).
May 18, 2018 - 04:04:08
Django version 2.0.2, using settings 'schedule_lessons.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

## Development Team

* [Ahmed Siddiqui](https://github.com/JeSuisAhmedN)
* [Shreyas Devalapurkar](https://github.com/sdevalapurkar)
* [Nisarg Patel](https://github.com/Nppatel97)
* [David Schriemer](https://github.com/CodemanDave)

## Contributors 

Thank you to all of our contributers who helped in the development of Schedulearn.

* [Lee Zeitz](https://github.com/LeeZeitz)
* [John Schriemer](https://github.com/jschriem)

