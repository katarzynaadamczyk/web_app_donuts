# web_app_donuts
Web app with dynamic programming algorithm and database. Under development.

Using docker, Flask, postgreSQL. 

App to get data from popular polish bakeries about donuts, then calculate for coming Fat Thursday how many of them a man can eat to maximize calories.

For now only works adding bakeries to database (endpoint /manufacturers_listing).

App is working on http:/localhost:5001/

To do:
- adding donuts to db 
- testing db
- adding user links to db 
- testing
- dp algorithm with showing results (infinite number of donuts available)
- html with choosing algorithm
- additional algorithms (for exaple only certain number of donuts are available)
- more tests
- add users (authorization and so on)
- adding data about user tests
- final tests




To work in venv:
python -m venv env
.\\venv\Scripts\activate.bat
set FLASK_APP=project/__init__.py
set FLASK_RUN_PORT=5001
pip install flask
python .\services\web\manage.py run
ctrl+c
deactivate

to activate project in docker:
cd katalog-repo
docker compose up

App is working on http:/localhost:5001/

aby sprawdzić działanie bazy danych można przy uruchomionym serwerze zrobić tylko ważne aby być w katalogu projektu:
cd KATALOG-REPO
docker compose exec web python manage.py seed_db
docker-compose exec db psql --username=hello_flask --dbname=hello_flask_dev
\c - informacja do jakiej bazy jesteśmy podpięci
\dt - lista tabel w aktualnej bazie danych
\l - lista baz danych
SQL (np. select * from table;)
\q - wyjście 
