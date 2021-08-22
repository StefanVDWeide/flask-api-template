# Flask REST API Template
A basic template to help kickstart development of a pure Flask API. This template is completely front-end independent 
and leaves all decisions up to the developer. The template includes basic login functionality based on JWT checks. 
How this token is stored and sent to the API is entirely up to the developer.

## Features
* Minimal Flask 2.X App
* Async/Await Functionallity
* Unit tests
* Basic Type Hints
* Integration With Redis For Background Tasks
* App Structured Using Blueprints
* Application Factory Pattern Used
* Authentication Functionality Using JWT
* Basic Database Functionality Included (SQLite3)
* Rate Limiting Functionality Based on Flask-Limiter For All The Routes In The Authentication Blueprint
* Support for .env and .flaskenv files build in


### Application Structure

The API is divided in six blueprints `auth`, `comments`, `errors`, `posts`, `tasks` and `users`.

The `auth` blueprint is responsible for all the routes associated with user registration and authentication.

The `comments` blueprint is responsible for handeling all requests related to comments, suchs as GET, POST and DELETE requests.

The `errors` blueprint is used to catch all errors and return the correct information.

The `posts` blueprint, just like the `comments` one, is responsible for handeling all requests related to posts, suchs as GET, POST and DELETE requests.

The `tasks` blueprint is responsible for requests related to asynchronous background tasks. Such as launching, retrieving the status of a specific task and retrieving all completed tasks.

The `users` blueprint handles the user related requests. Currently there are two routes which return either information ahout the current user or a different user based on username.

## Installation

##### Template and Dependencies

* Clone this repository:

	```
	$ git clone https://github.com/stefanvdw1/flask-api-template.git
	```

### Virtual Environment Setup

It is preferred to create a virtual environment per project, rather then installing all dependencies of each of your 
projects system wide. Once you install [virtual env](https://virtualenv.pypa.io/en/stable/installation/), and move to 
your projects directory through your terminal, you can set up a virtual env with:

```bash
python3 -m venv .venv
```

### Dependency installations

To install the necessary packages:

```bash
source venv/bin/activate
pip3 install -r requirements.txt
```

This will install the required packages within your venv.

---

### Setting up a SQLite3 Database

Database migrations are handled through Flask's Migrate Package, which provides a wrapper around Alembic. Migrations are done for updating and creating necessary tables/entries in your database. Flask provides a neat way of handling these. The files generate by the migrations should be added to source control.

To setup a SQLite3 database for development (SQLite3 is **not** recommended for production, use something like PostgreSQL or MySQL) you navigate to the folder where `flask_api_template.py` is located and run:

```bash
export FLASK_APP=flask_api_template.py
```

then you need to initiate your database and the migration folder with the following commands:

```bash
flask db init
```

```bash
flask db migrate "Your message here"
```

```bash
flask db upgrade
```

### Migrations

To make changes to the database structure you can also use the `flask db` commands:

```bash
export FLASK_APP=flask_api_template.py
```

```bash
flask db migrate -m "Your message here"
```

```bash
flask db upgrade
```

---

## Running the Application

Once you have setup your database, you are ready to run the application.
Assuming that you have exported your app's path by:

```bash
export FLASK_APP=flask_api_template.py
```

You can go ahead and run the application with a simple command:

```bash
flask run
```

---

## PostgreSQL
TODO

## Gunicorn
TODO

## Conclusion

Hopefully this template will inspire you to use Flask for your future API projects. If you have any feedback please do let me know or feel free to fork and raise a PR. I'm actively trying to maintain this project so pull request are more than welcome.

### Todo's and Improvements

- [x] Add request limiter
- [x] Add support for enviroment variables
- [x] Add async functionality
- [X] Add marshmallow validation for payloads
- [X] Add type hints
- [X] Add redis support and background workers
- [X] Add GitHub actions to run tests
- [x] Add GitHub action to check requirements using Dependabot
- [] Add tests for background tasks
- [] Add instructions to deploy to a production


## Acknowledgements
[Flask Mega Guide - Miguel Grinberg](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
