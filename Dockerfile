FROM       library/python:3.7.0
MAINTAINER  Hirotaka Ichikawa <hichtakk@gmail.com>

RUN git clone https://github.com/hichtakk/uketorikun.git && \
	cd /uketorikun && python /uketorikun/setup.py install
#COPY slackbot_settings.py /uketorikun/slackbot_settings.py
#COPY service_account.json /etc/uketorikun/

CMD python /uketorikun/run.py
