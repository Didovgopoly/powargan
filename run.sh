#!/bin/zsh

mkdir -p src/povargan-server/trained/
python util/GDriveDL.py https://drive.google.com/file/d/1YUwgZ-8ZH4pCr3aml-sP3bCkRLx5hIRz/view?usp=sharing src/povargan-server/trained/
python util/GDriveDL.py https://drive.google.com/file/d/1arS8WpnsAmSKA4xUgP195I2PEMnSUXTm/view?usp=sharing src/povargan-server/trained/ 
python util/GDriveDL.py https://drive.google.com/file/d/1YjzHUiBj1-m4aNddj10sv_2-AAtFu2QA/view?usp=sharing src/povargan-server/trained/
python util/GDriveDL.py https://drive.google.com/file/d/1m1k5HGESSTCzAMT8EgpeKFUUxLlzS6a_/view?usp=sharing src/povargan-server/trained/

# для 256
# cp /y src/povargan-server/model/netg_256.py src/povargan-server/model/netg.py
# python util/GDriveDL.py https://drive.google.com/file/d/1xnVskxNBiE-_SUnGYYIh69DP5dXdZvxD/view?usp=sharing src/povargan-server/trained/

# для 128
cp /y src/povargan-server/model/netg_128.py src/povargan-server/model/netg.py
python util/GDriveDL.py https://drive.google.com/file/d/11TR-z4RoQYSsR7oUXy7byCl4HX9uD3jF/view?usp=sharing src/povargan-server/trained/


# resnet
python util/GDriveDL.py https://drive.google.com/file/d/1udslmO77CcvKKnfY7y-NkbleqC0QsfOz/view?usp=sharing src/povargan-server/trained/
python util/GDriveDL.py https://drive.google.com/file/d/1qjQW3MUfOc46bEYPIzeFT1wXqJfEIEPJ/view?usp=sharing src/povargan-server/trained/



docker-compose build
docker-compose up
