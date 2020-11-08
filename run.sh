#!/bin/zsh

mkdir -p src/povargan-server/trained/rubert/ 
python util/GDriveDL.py https://drive.google.com/open?id=1Chs5wTGs1RV8Xi9IYow1m3mv5Fq02IrE src/povargan-server/trained/rubert/ 
python util/GDriveDL.py https://drive.google.com/open?id=1CsZOFgsBrt76a1yWDUBH1jmeGfpEzQQa src/povargan-server/trained/rubert/ 
python util/GDriveDL.py https://drive.google.com/open?id=1G8Tw31imbTugYtQ9c6Ylq5OPnIt1ZPtW src/povargan-server/trained/
docker-compose build
docker-compose up
