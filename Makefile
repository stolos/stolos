init:
	pip install -r requirements.txt

dev:
	./manage.py runserver 0.0.0.0:${PORT}

migrate:
	./manage.py migrate

makemigrations:
	./manage.py makemigrations

shell:
	./manage.py shell

watch:
	./manage.py watch

test:
	./manage.py test

worker:
	celery -A sister_watchd worker -l info
