# web_app_donuts
Web app with dynamic programming algorithm and database. Under development.

Using docker, Flask, postgreSQL. 

Under development.

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

aby sprawdzić działanie bazy danych można przy uruchomionym serwerze zrobić:

docker compose exec web python manage.py seed_db
docker-compose exec db psql --username=hello_flask --dbname=hello_flask_dev
\c - informacja do jakiej bazy jesteśmy podpięci
\dt - lista tabel w aktualnej bazie danych
\l - lista baz danych
SQL (np. select * from table;)
\q - wyjście 
