#!/bin/bash

node /home/pi/Documents/raspberry-dgc/validatorServer/app.js &
python3 /home/pi/Documents/raspberry-dgc/cameraClient/app.py
