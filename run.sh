#!/bin/zsh
dfgan=11TR-z4RoQYSsR7oUXy7byCl4HX9uD3jF

mkdir -p src/povargan-server/trained/

# w2v
./dl.sh 1YUwgZ-8ZH4pCr3aml-sP3bCkRLx5hIRz src/povargan-server/trained/food_w2v_300.w2v
./dl.sh 1arS8WpnsAmSKA4xUgP195I2PEMnSUXTm src/povargan-server/trained/w2tag.pkl
# lstm
./dl.sh 1YjzHUiBj1-m4aNddj10sv_2-AAtFu2QA src/povargan-server/trained/title_ingr_text_encoder.pth
./dl.sh 1m1k5HGESSTCzAMT8EgpeKFUUxLlzS6a_ src/povargan-server/trained/steps_text_encoder.pth
# dfgan 128
./dl.sh $dfgan src/povargan-server/trained/dfgan_128.pth
# resnet
./dl.sh 1udslmO77CcvKKnfY7y-NkbleqC0QsfOz src/povargan-server/trained/title_ingr_image_encoder.pth
./dl.sh 1qjQW3MUfOc46bEYPIzeFT1wXqJfEIEPJ src/povargan-server/trained/steps_image_encoder.pth

docker-compose build
docker-compose up
