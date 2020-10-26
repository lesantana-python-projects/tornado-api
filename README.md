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