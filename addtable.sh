#!/usr/bin/env bash
python3 manage.py makemigrations testsite
python3 manage.py migrate testsite
