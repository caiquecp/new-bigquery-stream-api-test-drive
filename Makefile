include .env
export $(shell sed 's/=.*//' .env)

.PHONY: install run format lint build-proto

install:
	pip install -r requirements.txt

run:
	python -m app

format:
	black app
	isort app

lint:
	mypy app
	flake8 app

build-proto:
	protoc -I ./proto_messages --python_out ./app ./proto_messages/customer.proto