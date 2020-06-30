# Flask REST API Template
A basic template to help kickstart development of a Flask API. This template is completely front-end independent and 
leaves all decisions up to the developer. The template includes basic login functionality based on JWT checks. How this 
token is stored and sent to the API is entirely up to the developer.

## Features
* Minimal Flask 1.X App
* App Structured Using Blueprints
* Application Factory Pattern Used
* Authentication Functionality Using JWT
* Basic Database Functionality Included (SQLite3)
* Rate Limiting Functionality Based on Flask-Limiter For All The Routes In The Authentication Blueprint


### Application Structure

The API is divided in a three main blueprints `auth`, `errors` and `main`.

The `auth` blueprint is responsible for all the routes associated with user registration and authentication.

The `errors` blueprint is used to catch all errors and return the correct information.

The `main` blueprint is an (almost) empty blueprint used as a placeholder for the main functionality of applicatons based on this template. Currently there are two routes which return either information ahout the current user or a different user based on username.

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
virtualenv venv
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

## Conclusion

Hopefully this template will inspire you to use Flask for your future API projects. If you have any feedback please do let me know or feel free to fork and raise a PR. I'm actively trying to maintain this project so pull request are more than welcome.

### Todo and Improvements

- [x] Add request limiter
- [x] Add tests
- [] Add support for PostgreSQL database
- [] Add support for a production server using gunicorn
