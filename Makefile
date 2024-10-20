# Makefile

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

prune:
	docker system prune --all --force --volumes
	docker builder prune -f

run:
	docker compose up -w; docker compose rm -f -v

test:
	pytest -v backend/tests/

testless:
	pytest -v backend/tests/ | less
