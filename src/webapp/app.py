from time import sleep
import random

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app=app)

examples = [
    'static/img/example.jpg',
    'static/img/example2.jpg',
    'static/img/example3.jpg',
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate-image', methods=['post'])
def handle_generate_request():
    text = request.form['text']
    sleep(1)
    generated_img_path = random.choice(examples)

    generation_request = GenerateRequest(text, generated_img_path)
    db.session.add(generation_request)
    db.session.commit()

    resp = jsonify({
        'id': generation_request.id,
        'img': generated_img_path
    })

    return resp


class GenerateRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    generated_img_path = db.Column(db.String(), nullable=True)

    def __init__(self, text, generated_img_path):
        self.text = text
        self.generated_img_path = generated_img_path

    def __repr__(self):
        return '<GenerateRequest %r>' % self.text


if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000)
