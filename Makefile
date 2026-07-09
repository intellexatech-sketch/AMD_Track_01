.PHONY: setup test run docker-up docker-down

setup:
	pip install -r requirements.txt

test:
	pytest tests/ -v

run:
	uvicorn app.main:app --reload

docker-up:
	docker-compose up --build -d

docker-down:
	docker-compose down
