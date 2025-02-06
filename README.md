# web_app_donuts
Web application in Flask integrated with postgreSQL database working in Docker container. Gets data about donuts from given URL's and adds it to database. Calculates which donuts are to be bought to maximize calories on Fat Thursday using dynamic programming.


## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Tests setup](#tests-setup)
* [Status](#status)
* [Inspiration](#inspiration)
* [Notes](#notes)


## General info

Actually (6/2/2025) works adding bakeries and donuts to the database by reading data from web pages listed in database.json. Two endpoints also work:

- endpoint /donuts_listing lists all donuts on web page
- endpoint /manufacturers_listing lists all manufacturers on web page

Idea from task from flynerd.pl: 

https://www.flynerd.pl/2019/02/tlusty-python-z-paczkami-i-algorytmami.html


## Technologies

* Python 3 - version 3.12.9
* Flask - version 3.1.0
* Pytest 8.3.4
* Docker
* flask_sqlalchemy - version 3.1.1
* bs4 - BeautifulSoup - version 0.0.2
* gunicorn - version 23.0.0
* requests - version 2.32.3


## Setup

I use CMD for activating venv:

To work in venv:

cd project_catalogue\services\web

python -m venv env

.\\venv\Scripts\activate.bat

set FLASK_APP=project/__init__.py

set FLASK_RUN_PORT=5001

pip install flask

python .\services\web\manage.py run

ctrl+c

deactivate


To activate project in docker:

cd project_catalogue

docker compose up

App is working on http:/localhost:5001/

To shut it down: ctrl+c


To activate production server - I have not checked it yet. For test environment there is an .env file in repository, but to work in production server you will need to create your own .env.prod and .env.prod.db files.


## Tests setup

To activate tests you need to write following commands in CMD:

cd project_catalogue

cd services

cd web

python -m venv venv

.\venv\Scripts\activate.bat

pip3 install -r tests\requirements.txt

pytest

deactivate


## Status
Under development.

To do:

- dp algorithm with showing results (infinite number of donuts available)
- testing
- html with choosing algorithm
- additional algorithms (for example only certain number of donuts are available)
- more tests
- add users (authorization and so on)
- adding data about user's checking donuts to buy
- check production server
- final tests
- final readme update


## Inspiration

Idea from task from flynerd.pl: 

https://www.flynerd.pl/2019/02/tlusty-python-z-paczkami-i-algorytmami.html


## Notes

Data from given web pages are used only in learning process, not for commercial use.

