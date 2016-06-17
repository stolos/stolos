init:
	pip install -r requirements.txt

dev:
	./manage.py runserver 0.0.0.0:${PORT}

migrate:
	./manage.py migrate

makemigrations:
	./manage.py makemigrations

test:
	./manage.py test
