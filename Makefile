dev:
	python setup.py develop

install:
	python setup.py install

run:
	python ./run.py

docker:
	sudo docker build -t hichtakk/uketorikun .

docker-run: docker
	sudo docker run -it -e TZ=US/Pacific -v ${PWD}/service_account.json:/etc/uketorikun/service_account.json -v ${PWD}/slackbot_settings.py:/uketorikun/slackbot_settings.py hichtakk/uketorikun
