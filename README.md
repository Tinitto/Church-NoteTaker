# Church NoteTaker API
---
A simple note taking app **Browserable API** for cell-based churches to take both personal and public notes in cell meetings and share them across all cells of the church

## Dependencies
- [Django](https://djangoproject.com) (written in version 1.11.4)
- [Django Rest Framework](http://www.django-rest-framework.org) (written in version 3.6.3)
- [Python](https://www.python.org) (version 3.5+)
- [Markdown](http://pythonhosted.org/Markdown/install.html) (2.1.0+)
- [Django Framework JWT Authentication](https://github.com/GetBlimp/django-rest-framework-jwt)
- [Postgresql Database Engine](https://www.postgresql.org) (with psycopg2 python package)
- [Django Cities Light](https://django-cities-light.readthedocs.io/en/stable-3.x.x/)

## How to Install
- Make sure you have the above dependencies in your [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
- Clone the repo

  ```$ git clone <the repo's url> notertaker```
- Set up the Postgresql database, user and update the settings file in your local clone
- In your shell/terminal, activate your virtualenv (the code snippet is for those on linux)

  ```$ source path_to_virtualenv/bin/activate```
- In your shell/terminal, navigate to the folder where the repo clone is
- Still in your shell/terminal and initialize the api with the following commands (_make sure you are in the root of your folder where manage.py is_)

  ```$ python manage.py makemigrations ```

  ```$ python manage.py migrate ```

  ```$ python manage.py runserver```
- In order to pre-fill the django-cities-light data, you will have to run the command

  ```$ python manage.py cities_light ```


## Apps
### 1. Oldcell
This is the main application containing the settings of the project. 

Take care to follow the appropriate deployment checklist for django in case you are to use this API in production

### 2. Location
This contains the extensions of the Django Cities Light to ease customization.

This application is to help users easily select their location during registration or when updating their profiles or those of the organizations they create.

_A program in an organization can be restricted to users from a given location (as well gender, age etc)_

### 3. User
This contains the models and serializers for the extended user model. It deals with registration of new users, their profiles, confirmation of their emails (this uses a commandline email engine. *Be sure to change this in settings.py in production*)

### 4. Organization
As you will soon find out, this api can be used by any organization even if it is not a church.

The Organization app contains the models, serializers, permissions and views that allow for the following features of the api:
- Select type of organization i.e. whether church, NGO, company etc.
- Ability of the SuperUsers to add any new organization category at any time
- Creation of Organization by any user. On creation, the organization cannot be seen by anyone else until approved by Staff (_The approval implementation is yet to be integrated_)
- The organization creator can add any existing users as administrators of the organization
- The organization creator and administrators can add new programs under that organization

### 5. Program
This corresponds to a single cell or a single department. A cell can be a child of another cell (read 'program')

The models. serializers, views and permissions in this app allow for the following features:
- An organization admin/creator can create a new program
- An organization admin/creator can add new users to the program
- An organization admin/creator can give a member of a program any of the roles of Admin, Editor or Normal user (normal user is the default)
- A program admin can add new users to the program and allocate roles to the program's members
- A program editor can create and edit agendas for any meeting

### 6. Minutes
This is the heart of the API. This holds the models, views, serializers and permissions for agendas, minutes (topics and points) and references to any book (esp. the Bible but other books are also allowed), website url etc.

The features include:
- A program editor can create a new agenda visible to all users by default. 
- Only the program editor or admin can create an agenda and add topics (or minute titles)
- Only the members of the program to which the editor belongs can write points to each topic (or minute)
- Points written by a user can be set as private to the user only or to the group but are by default publicly visible to all users of the platform
- A topic (called minute in the models) can have any number of references to any book, website url etc.
- A point to any minute topic can have a number of references to any book, website url etc.

## ToDo
A number of things are yet to be added.
- Feature to allow staff approve or deny organizations registered
- Feature to allow users react to any point or minute topic (by agreeing, disagreeing or reporting as inappropriate)
- An application to allow staff to moderate and provide support e.g. responding to reported points, minutes
- A commenting system to allow users to comment on each point based on the privacy setting of the point
- Addition of media (e.g. a photo, video, audio) to a given point or minute topic
- The frontend (mobile and web) to accompany the API
- The full deployment guide using gunicorn, Nginx, Postgresql, Ubuntu 16.04
- Tests in each application
- A proper full documentation of the API

## News
I am currently unable to actively develop this API to full completion as quickly as I had hoped due to other pressing obligations.

I thus welcome any pull requests. Ensure that your code follows the PEP8 guidelines and is appropraitely commented so that I can quickly add it in if it is relevant.

