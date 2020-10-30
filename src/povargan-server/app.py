from time import sleep
import random
import base64

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
examples = [
    'static/img/example.jpg',
    'static/img/example2.jpg',
    'static/img/example3.jpg',
]


@app.route('/generate-image', methods=['get'])
def handle_generate_request():
    request_text = request.form['text']
    print(request_text)
    sleep(1)
    generated_img_path = random.choice(examples)

    with open(generated_img_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    
    resp = jsonify({
        'img': encoded_string
    })

    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
