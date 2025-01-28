# web_app_donuts
Web app with dynamic programming algorithm and database. Under development.

Using docker, Flask, postgreSQL. 



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

Potem działa na aplikacja działa na http:/localhost:5001/

aby sprawdzić działanie bazy danych można przy uruchomionym serwerze zrobić tylko ważne aby być w katalogu projektu:
cd KATALOG-REPO
docker compose exec web python manage.py seed_db
docker-compose exec db psql --username=hello_flask --dbname=hello_flask_dev
\c - informacja do jakiej bazy jesteśmy podpięci
\dt - lista tabel w aktualnej bazie danych
\l - lista baz danych
SQL (np. select * from table;)
\q - wyjście 
