include backend/.env

build_frontend:
	cd frontend  && npm i && npm run build

init_app: build_frontend
	docker compose --env-file=backend/.env up -d

down:
	docker compose --env-file=backend/.env down
