# Schedulearn

A web app that tutors and students can use to schedule lessons efficiently with each other.

The service is available for free use at `https://www.schedulearn.com`

## Running the Application Locally

### NOTE: This project is using python 3.6.5 and Django 2.0.6

a. Using your terminal or command prompt, navigate to your workspace directory.

b. You need to clone our repo on the terminal. You can do this by the following command:

```bash
#!/bin/bash
$ git clone https://github.com/sdevalapurkar/schedulearn.git
```

c. Assuming you have python3.6.5 installed, you can install our dependencies using pip.

#### Side note: We recommend you install these dependencies in a virtual environment, although this isn't necessary

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

##### You can now go to IP address that the app is running on in your browser

NOTE: You can make changes to the code while the server is running and the new code will show up as soon as you refresh your browser, you don't need to restart the server. HOWEVER, in the advanced case you make changes to the database (models.py), you will need to migrate those changes. Additonally, changes to the css files may not show up even if you refresh your browser, this can be because your browser is storing cache files of the css (HINT: try holding shift and refreshing your browser).

## Development Team

* [Ahmed Siddiqui](https://github.com/JeSuisAhmedN)
* [Shreyas Devalapurkar](https://github.com/sdevalapurkar)
* [Lee Zeitz](https://github.com/LeeZeitz)
* [Nisarg Patel](https://github.com/Nppatel97)
* [John Schriemer](https://github.com/jschriem)
* [David Schriemer](https://github.com/CodemanDave)

## Screenshots

<img width="1257" alt="pending" src="https://user-images.githubusercontent.com/28017034/37558880-7825830c-29d8-11e8-84a1-1b46f3c08e57.png">

When a student schedules a lesson, the tutor can confirm or decline the request.

<img width="1250" alt="confirm" src="https://user-images.githubusercontent.com/28017034/37558872-5f74557c-29d8-11e8-9a17-b894820f79ea.png">

Login page

<img width="428" alt="login" src="https://user-images.githubusercontent.com/28017034/37558878-77f9cd3e-29d8-11e8-9f43-920a66ddfc3d.png">

See a list of tutors and add tutors to this list

<img width="599" alt="mytutors" src="https://user-images.githubusercontent.com/28017034/37558879-780eac90-29d8-11e8-9599-a9b556b6a3b9.png">

Check the availability of a tutor before scheduling a lesson.

<img width="1250" alt="avail" src="https://user-images.githubusercontent.com/28017034/37558893-ba94fee8-29d8-11e8-8489-eaf54b3e648e.png">
