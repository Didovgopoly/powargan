#!/bin/zsh
google_id=$1
fn=$2
cookies=/tmp/cookies.txt
a=$(wget --quiet --save-cookies $cookies --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id='$google_id -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$a&id=$google_id" -O $fn && rm -rf $cookies
#google_id=1qjQW3MUfOc46bEYPIzeFT1wXqJfEIEPJ
#fn=/tmp/model.pth


