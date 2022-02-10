SHELL=/usr/bin/bash

#Variable
APP_NAME=app


build:
	docker build -t ${APP_NAME} .
	

run:
	docker run -it --rm -name running-${APP_NAME} ${APP_NAME}
