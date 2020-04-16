.PHONY: build run test tox

build:
	docker-compose build

run:
	docker-compose up -d

makemigrations:
	docker-compose run web python manage.py makemigrations

test:
	docker-compose run web python manage.py test

shell:
	docker-compose run web python manage.py shell

