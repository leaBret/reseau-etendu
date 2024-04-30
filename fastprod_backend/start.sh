#!/bin/bash

# pipenv shell
pipenv install flask
pipenv install nornir
pipenv install pyyaml
pipenv install nornir_utils
pipenv install nornir_napalm
pipenv install nornir_netmiko
export FLASK_APP=fastprod/api
export FLASK_DEBUG=1
flask run