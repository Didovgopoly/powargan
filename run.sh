#!/bin/zsh
dfgan=1PtOjUqImOPnGF6sEg60Al5JodLUBvF7n

mkdir -p src/povargan-server/trained/

# w2v
sh ./dl.sh 1YUwgZ-8ZH4pCr3aml-sP3bCkRLx5hIRz src/povargan-server/trained/food_w2v_300.w2v
sh ./dl.sh 1arS8WpnsAmSKA4xUgP195I2PEMnSUXTm src/povargan-server/trained/w2tag.pkl
# lstm
sh ./dl.sh 1YjzHUiBj1-m4aNddj10sv_2-AAtFu2QA src/povargan-server/trained/title_ingr_text_encoder.pth
sh ./dl.sh 1m1k5HGESSTCzAMT8EgpeKFUUxLlzS6a_ src/povargan-server/trained/steps_text_encoder.pth
# dfgan 128
sh ./dl.sh $dfgan src/povargan-server/trained/dfgan_128.pth
# resnet
sh ./dl.sh 1vuLjcJ9JbMyJj61kiPm_lXZ5rpyvuubw src/povargan-server/trained/title_ingr_image_encoder.pth
sh ./dl.sh 1km6h4G2fvXbwve6s_trCZcHBNmI6CkSC src/povargan-server/trained/steps_image_encoder.pth

docker-compose build
docker-compose up
