DC = docker compose
LOGS = docker logs
EXEC = docker exec -it
ENV = --env-file .env
APP_FILE = docker_compose/app.yaml
STORAGES_FILE = docker_compose/storages.yaml
APP_CONTAINER = main-app

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down

.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} bash

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV} up --build -docker

.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} down

.PHONY: all
all:
	${DC} -f {APP_FILE} -f ${STORAGES_FILE} ${ENV} up --build -docker

.PHONY: test
test:
	${EXEC} ${APP_CONTAINER} pytest
