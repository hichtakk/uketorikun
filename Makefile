dev:
	python setup.py develop

install:
	python setup.py install

run:
	python ./run.py

docker:
	sudo docker build -t hichtakk/uketorikun .
