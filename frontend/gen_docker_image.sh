#!/bin/bash

flutter pub get
flutter build web

docker build --no-cache -t fast_web_app .