WEB_CONCURRENCY?=3
PORT?=8000

init:
	pip install -r requirements.txt

dev:
	python manage.py runserver 0.0.0.0:${PORT}

migrate:
	python manage.py migrate --no-input

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

dumpdata:
	@ python manage.py dumpdata projects.server projects.stack auth.permission auth.user auth.group --indent=2

loaddata:
	python manage.py loaddata fixture.json

bootstrap: migrate loaddata

collectstatic:
	python manage.py collectstatic --no-input --ignore=node_modules --ignore=src --link

prod: migrate collectstatic
	PROD=1 gunicorn stolosd.wsgi --bind=0.0.0.0:${PORT} --workers=${WEB_CONCURRENCY} --threads=2 --max-requests=10000 --access-logfile=-
