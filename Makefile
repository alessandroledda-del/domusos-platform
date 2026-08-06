up:
	docker compose up --build

down:
	docker compose down

migrations:
	docker compose exec backend sh scripts/generate_migrations.sh

migration-check:
	docker compose exec backend python manage.py makemigrations --check --dry-run
	python scripts/check_migrations.py

migrate:
	docker compose exec backend python manage.py migrate

superuser:
	docker compose exec backend python manage.py createsuperuser

catalog:
	docker compose exec backend python manage.py seed_catalog

demo:
	docker compose exec backend python manage.py seed_demo

test:
	docker compose exec backend sh -c "DJANGO_SETTINGS_MODULE=config.settings_test python manage.py test"

release-check:
	python scripts/check_release.py
	python scripts/check_migrations.py

production-up:
	docker compose -f docker-compose.production.yml up -d --build
