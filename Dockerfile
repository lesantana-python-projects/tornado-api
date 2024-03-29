FROM python:3.8.5

WORKDIR /opt/weather

RUN mkdir -p /opt/weather/logs

RUN apt-get update --upgrade
RUN apt-get -y install git vim openssh-client gcc python3-dev \
    libevent-dev libblas-dev libatlas-base-dev \
    libsasl2-dev python-dev libldap2-dev libssl-dev python-psycopg2 \
    libpq-dev python3-psycopg2 supervisor unzip wget nodejs

ENV PIPENV_VERBOSITY=-1
ENV VIRTUAL_ENV "/venv"
RUN python -m venv $VIRTUAL_ENV
ENV PATH "$VIRTUAL_ENV/bin:$PATH"

COPY ./main.py /opt/weather
COPY ./supervisor.conf /etc/supervisor/conf.d/
COPY ./Pipfile /opt/weather
COPY ./Pipfile.lock /opt/weather
COPY ./manager.py /opt/weather
COPY ./Makefile /opt/weather

RUN python -m pip install -U pip

RUN python -m pip install pipenv

RUN python -m pipenv install --dev

EXPOSE 80

ENTRYPOINT ["supervisord", "-c", "/etc/supervisor/conf.d/supervisor.conf"]