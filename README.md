# schedule-my-lessons
A web app that tutors and students can use to interact with each other and easily schedule/manage all their lessons

## Try it out

If you want to see our work in action, visit: schedulearn.com

Otherwise, if you'd like to run a test module and play around with our code, complete the following steps:

1- Using your terminal or command prompt, navigate to your workspace directory such as the following:

```
$ cd Desktop
$ cd Workspace
```

2- Next, you need to clone our repo on the terminal. You can do this by the following command:
NOTE: $ sign at the beginning denotes the terminal, you don't type that in

```
$ git clone https://github.com/sdevalapurkar/schedule-my-lessons.git
```

OR if you would like to clone from a specific branch, then the following command will do:

```
$ git clone -b [INSERT_BRANCH_NAME] https://github.com/sdevalapurkar/schedule-my-lessons.git
```

3- Navigate inside our repo:

```
$ cd schedule-my-lessons
$ cd schedule_lessons
```

4- Now you want to run our app locally on your computer, you can do this using the following command:
NOTE: This part might give you an error as you need to install django for this work. If you get an error, we recommend you make a virtual environment and install django in that virtual enviornment, and THEN run this command (For more info, check out the following video: https://www.youtube.com/watch?v=c2zTxSqHTc8)

```
$ python manage.py runserver
```

After running that command, you should get the following output: 

```
Performing system checks...

System check identified no issues (0 silenced).
May 18, 2018 - 04:04:08
Django version 2.0.2, using settings 'schedule_lessons.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

5- You can now go to IP address that the app is running on (in our case: http://127.0.0.1:8000/) in your browser

NOTE: You can make changes to the code while the server is running and the new code will show up as soon as you refresh your browser, you don't need to restart the server. HOWEVER, in the advanced case you make changes to the database (models.py), you will need to migrate those changes. Additonally, changes to the css files may not show up even if you refresh your browser, this can be because your browser is storing cache files of the css (HINT: try holding shift and refreshing your browser).

## Authors

* [Lee Zeitz](https://github.com/LeeZeitz)
* [Shreyas Devalapurkar](https://github.com/sdevalapurkar)
* [Ahmed Siddiqui](https://github.com/JeSuisAhmedN)
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
