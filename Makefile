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

# Run pytest with verbose output and pipe to less for easier reading
test:
	pytest -v backend/tests/

test less:
	pytest -v backend/tests/ | less
