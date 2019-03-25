.PHONY: dev install run docker release docker-run

VERSION := $(shell cat ./uketorikun/__init__.py | sed -e "s/.*'\(.*\)'.*/\1/g")

DOCKERHUB_ID := hichtakk
IMAGE_NAME := uketorikun
IMAGE_REPOSITORY := ${DOCKERHUB_ID}/${IMAGE_NAME}:v${VERSION}


dev:
	python setup.py develop

install:
	python setup.py install

run:
	python ./run.py

check:
	@echo checking package vulnerability
	pipenv check

docker:
	sudo docker build -t hichtakk/uketorikun:v$(VERSION) .

release:
	@docker login
	@docker push ${IMAGE_REPOSITORY}

docker-run:
	sudo docker run -it -d -e TZ=US/Pacific \
		-v ${PWD}/service_account.json:/etc/uketorikun/service_account.json \
		-v ${PWD}/slackbot_settings.py:/uketorikun/slackbot_settings.py \
		$(IMAGE_REPOSITORY)

