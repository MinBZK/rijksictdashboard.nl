include .env

up:
	docker compose --env-file=.env up -d

down:
	docker compose --env-file=.env down

drop_db:
	docker run --rm -i --env PGPASSWORD=${POSTGRES_PASSWORD} postgres dropdb --if-exists -U ${POSTGRES_USER} -p ${POSTGRES_PORT} -h host.docker.internal '${POSTGRES_DB}' -f --if-exists

init_db: up
	python -c "import time; time.sleep(5)"
	docker run --rm -i --env PGPASSWORD=${POSTGRES_PASSWORD} -v ${CURDIR}/dev_db:/dump/ postgres psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -p ${POSTGRES_PORT} -h host.docker.internal -f /dump/schema.sql

server:
	poetry run uvicorn app.main:app --reload --port 8000
