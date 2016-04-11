#!/usr/bin/env bash
#$1 - param for specific environment: local | main

if [[ "$1" == "main" ]]; then
    ENV=$1
else
    ENV=local
fi

echo ${ENV} settings
pip3 install -r ./requirements/${ENV}.pip
python3 -m manage migrate --settings=simple_app.settings.${ENV}
echo Creation of superuser
python3 -m manage createsuperuser --username=manager --email=manager@simpleapp.com \
    --settings=simple_app.settings.${ENV}
python3 -m manage runserver --settings=simple_app.settings.${ENV}
