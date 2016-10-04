init:
	pip install -r requirements.txt

dev:
	python manage.py runserver 0.0.0.0:${PORT}

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

shell:
	python manage.py shell

watch:
	python manage.py watch

test:
	python manage.py test

worker:
	celery -A stolosd worker -l info

loaddata:
	python manage.py loaddata fixture.json

bootstrap: migrate loaddata
