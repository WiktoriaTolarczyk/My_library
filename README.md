{% if False %}

# Introduction

The main task of the application is to collect information about books that the registered user owns, has borrowed or intends to buy. 

Each of these categories has its own functionality,which allows the user to select dedicated options. 

You can add items to the main catalog, which is a collection of all books that are currently in the user's possession (including books borrowed from the library), modify the corresponding data (including adding reviews, rating on a scale of 1-10), deleting or create your own reading plans, to which you can add books previously included in the collection.

The section dedicated to borrowed books contains all books added by the user, divided into libraries. You can extend their deadlines and mark their submission status. 

The section dedicated to books intended for purchase collects prices in a database. You can mark the purchase of a book in the application; then the given item is automatically transferred to the user's shelf along with data regarding the purchase details. 

There are also sections related to:
-  the user's reading plans,
-  visualization of statistical data related to user activity in the application.

It is strongly recommended to look at working_app gif at the beginning to have an initial look at the main functionality of the application!

![Default Home View](__screenshots/main_view.png?raw=true "Main View")


# Usage

To use this template to start your own project:

### Existing virtualenv

If your project is already in an existing python3 virtualenv first install django by running

    $ pip install django
    
And then run the `django-admin.py` command to start the new project:

    $ django-admin startproject --template https://github.com/WiktoriaTolarczyk/My_library/archive/refs/heads/main.zip new_django_project .
      
### No virtualenv

This assumes that `python3` is linked to valid installation of python 3 and that `pip` is installed and `pip3`is valid
for installing python 3 packages.

Installing inside virtualenv is recommended, however you can start your project without virtualenv too.

If you don't have django installed for python 3 then run:

    $ pip3 install django
    
And then:

    $ django-admin startproject --template https://github.com/WiktoriaTolarczyk/My_library/archive/refs/heads/main.zip new_django_project .
      
      
After that just install the local dependencies, run migrations, and start the server.

{% endif %}

# My_library

# Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone https://github.com/WiktoriaTolarczyk/My_library.git
    $ cd My_library
    
Activate the virtualenv for your project.
    
Install project dependencies:

    $ pip install -r requirements.txt


Set default database in MyLibraryApp/settings.py:

![Default DB Settings](__screenshots/db_settings.png?raw=true "DB settings")
    
    
Then simply apply the migrations:

    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver

## Run tests

You can use existing plugin pytest-django to run the tests related to My_library app; tests are created at MyLibraryApp/tests/test_django.py file.
To run the tests use:

    $ pytest tests