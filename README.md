# Gaivota Python Test

Install and activate virtualenv with version ```Python 3.8.5``` </br>
Install libs with pipenv install, follow command below.

```
$ pip install pipenv
$ pipenv sync
```
Steps to prepare database and content data:

```
$ python manager.py migrate
$ python manager.py content
```

To use sonarqube, follow instructions below.
For this is necessary to install any components, and you can try it.

```
$ docker run -d --name sonarqube -p 9000:9000 sonarqube:7.9.4-community

$ sudo apt-get update
$ sudo apt-get install unzip wget nodejs

$ sudo mkdir ./downloads/sonarqube -p
$ cd ./downloads/sonarqube
$ sudo wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.2.0.1873-linux.zip
$ sudo unzip sonar-scanner-cli-4.2.0.1873-linux.zip
$ sudo mv sonar-scanner-4.2.0.1873-linux /opt/sonar-scanner
```
Open sonar-scanner file and content bellow

```
$ sudo vim /etc/profile.d/sonar-scanner.sh
```
```
#/bin/bash
export PATH="$PATH:/opt/sonar-scanner/bin"
```
enable new configs
```
source /etc/profile.d/sonar-scanner.sh
sudo rm -rf ./downloads
```

After that you can try tests with coverage/sonar
```
$ make test-sonar

```

For the simple test without sonar, you can try this.
```
$ make test-coverage

```