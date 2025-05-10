#!/bin/bash

# Inicie o Gunicorn
exec gunicorn -w 1 -b 0.0.0.0:5000 run:app