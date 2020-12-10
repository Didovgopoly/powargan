@echo off
mkdir src\povargan-server\trained\
python util/GDriveDL.py https://drive.google.com/file/d/1YUwgZ-8ZH4pCr3aml-sP3bCkRLx5hIRz/view?usp=sharing src\povargan-server\trained\
python util/GDriveDL.py https://drive.google.com/file/d/1arS8WpnsAmSKA4xUgP195I2PEMnSUXTm/view?usp=sharing src\povargan-server\trained\ 
python util/GDriveDL.py https://drive.google.com/file/d/1YjzHUiBj1-m4aNddj10sv_2-AAtFu2QA/view?usp=sharing src\povargan-server\trained\
python util/GDriveDL.py https://drive.google.com/file/d/1m1k5HGESSTCzAMT8EgpeKFUUxLlzS6a_/view?usp=sharing src\povargan-server\trained\
python util/GDriveDL.py https://drive.google.com/file/d/1xnVskxNBiE-_SUnGYYIh69DP5dXdZvxD/view?usp=sharing src\povargan-server\trained\

docker-compose build
docker-compose up