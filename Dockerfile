FROM python:3.9.15-slim-buster

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y --no-install-recommends apt-utils
RUN apt-get update -y && apt-get install -y git build-essential postgresql-server-dev-all

RUN useradd -ms /bin/bash numbas_lti && usermod -a -G numbas_lti www-data

RUN mkdir /srv/numbas-lti-media /srv/numbas-lti-static
RUN chown -R numbas_lti:numbas_lti /srv/numbas-lti-media
RUN chown -R www-data:www-data /srv/numbas-lti-static
RUN chmod -R 777 /srv/numbas-lti-media /srv/numbas-lti-static

ARG VERSION=v3.2
RUN git clone --depth 1 --branch ${VERSION} https://github.com/numbas/numbas-lti-provider.git /opt/numbas-lti-provider
WORKDIR "/opt/numbas-lti-provider"
RUN chown -R numbas_lti:numbas_lti /opt/numbas-lti-provider
RUN chmod -R 770 /opt/numbas-lti-provider
RUN python3 -m pip install -r /opt/numbas-lti-provider/requirements.txt
RUN python3 -m pip install channels_redis==3.3.1 redis==3.5.3 psycopg2==2.8.6  django-environ==0.7.0

COPY files/numbas-lti-provider/settings.py /opt/numbas-lti-provider/numbasltiprovider/settings.py
