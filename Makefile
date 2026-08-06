up:
	docker compose up --build

down:
	docker compose down

migrate:
	docker compose exec backend python manage.py makemigrations
	docker compose exec backend python manage.py migrate

superuser:
	docker compose exec backend python manage.py createsuperuser

catalog:
	docker compose exec backend python manage.py seed_catalog

demo:
	docker compose exec backend python manage.py seed_demo

test:
	docker compose exec backend python manage.py test

logs:
	docker compose logs -f

worker-logs:
	docker compose logs -f worker

schema:
	docker compose exec backend python manage.py spectacular --file openapi.yml

production-up:
	docker compose -f docker-compose.production.yml up -d --build

production-down:
	docker compose -f docker-compose.production.yml down

smoke:
	sh scripts/pilot_smoke_test.sh
