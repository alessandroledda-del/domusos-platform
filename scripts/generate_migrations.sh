#!/usr/bin/env sh
set -eu
python manage.py makemigrations \
  accounts companies properties documents workflows audit reports \
  notifications catalog orders billing integrations compliance analytics \
  marketplace onboarding
python manage.py makemigrations --check --dry-run
