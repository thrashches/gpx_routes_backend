# Makefile

test:
	docker-compose exec server python manage.py test

start-local:
	docker-compose -f deploy/docker-compose.local.yml up -d --build

down-local:
	docker-compose -f deploy/docker-compose.local.yml down -v

logs-local:
	docker-compose -f deploy/docker-compose.local.yml  logs -f

