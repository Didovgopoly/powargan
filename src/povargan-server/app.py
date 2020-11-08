from time import sleep
import random
import base64

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

import uuid
import torchvision.utils as vutils
from model.rubert import transform
from model.netg import generate

import io
import torch
from PIL import Image


app = Flask(__name__)
cors = CORS(app)
examples = [
    'static/img/example.jpg',
    'static/img/example2.jpg',
    'static/img/example3.jpg',
]


@app.route('/generate-image', methods=['options'])
def handle_generate_request_options():
    sleep(1)        
    resp = jsonify({})
    resp.headers.add('Access-Control-Allow-Headers', '*')
    resp.headers.add('Access-Control-Allow-Origin', '*')   
    return resp

@app.route('/generate-image', methods=['post'])
def handle_generate_request():
    sleep(1)
    json = request.get_json()
    encoded_string = ""
    res = ""
    text = json['text']
    try:        
        title_emb = transform(text)
        fake = generate(title_emb,4)
        
        # generated_img_path = get_image_name("/result/")        
        # vutils.save_image(fake.data,generated_img_path,nrow=2, normalize=True)
        # with open(generated_img_path, "rb") as image_file:
        #     encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

        grid = vutils.make_grid(fake.data, nrow=2,normalize=True)
        ndarr = grid.mul(255).add_(0.5).clamp_(0, 255).permute(1, 2, 0).to('cpu', torch.uint8).numpy()
        im = Image.fromarray(ndarr)
        temp = io.BytesIO()
        im.save(temp, format="jpeg")
        encoded_string = base64.b64encode(temp.getbuffer()).decode("utf-8")

    except Exception as e:
        res = str(e)        

    resp = jsonify({
        'img': encoded_string,
        'txt': text,
        'res': res        
    })

    return resp

import datetime
import numpy as np
def get_image_name(d):
    basename = "image"
    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    filename = "_".join([basename, suffix,str(np.random.randint(1000))])+'.jpg' 
    return d+filename

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
