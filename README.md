# Tornado Python Test

For this project was used  ```Python 3.8.5``` </br>

First of all, you should execute docker-compose.

```
$ docker-compose up -d
```

After that, execute the commands below to create a database structure and our first content.

```
$ docker exec gaivotaApi python manager.py migrate
$ docker exec gaivotaApi python manager.py content
```

In this docker-compose configs, we have the technologies bellow

```
. Docker with our TornadoApi = http://localhost:8081/doc
. SonarQube = http://localhost:9000/
. Postgres Database = http://localhost:5432
. Postgres Admin = http://localhost:15432
```

To execute unit tests execute the command bellow. <br/>

The tests coverage is 100%  :)

```
docker exec gaivotaApi python -m pipenv run make tests
```
----------------------------------------------------------------------

You can use sonar-scanner to send the coverage to SonarQube and execute analysis <br/>

For that you can try the instructions bellow in your machine:

```
$ sudo apt-get update
$ sudo apt-get install unzip wget nodejs

$ sudo mkdir ./downloads/sonarqube -p

$ cd ./downloads/sonarqube
$ sudo wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.2.0.1873-linux.zip
$ sudo unzip sonar-scanner-cli-4.2.0.1873-linux.zip
$ sudo mv sonar-scanner-4.2.0.1873-linux /opt/sonar-scanner

$ sudo echo '#/bin/bash' >> /etc/profile.d/sonar-scanner.sh
$ sudo echo export PATH="$PATH:/opt/sonar-scanner/bin" >> /etc/profile.d/sonar-scanner.sh

$ source /etc/profile.d/sonar-scanner.sh
$ sudo rm -rf ./downloads

------------------- prepare developer environment python 3.8.5 ---------------------------------------

$ sudo apt-get update --upgrade
$ sudo apt-get -y install git vim openssh-client gcc python3-dev \
    libevent-dev libblas-dev libatlas-base-dev \
    libsasl2-dev python-dev libldap2-dev libssl-dev python-psycopg2 \
    libpq-dev python3-psycopg2 supervisor unzip wget nodejs

$ pip install pipenv
$ pipenv install --dev

$ make test-sonar

```