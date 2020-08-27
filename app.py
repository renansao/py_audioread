from flask import Flask, jsonify
from flask import request
from flask import abort
from readAudio import readAudio
from glob import glob
from transformText import transformToText
from functools import wraps
import jwt
from audioController import analyseAudioController
import sys
from sendEmail import send_email

app = Flask(__name__)
app.config['SECRET_KEY'] = "RraIY0negneEQzv3XO6kwjN4XVtsul1A"

#General Function to check for a JWT token in the request
def check_for_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'errorMessage':'Token Inválido'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return jsonify({'errorMessage':'Token Inválido'}), 403
        return func(*args, **kwargs)
    return wrapped

@app.route('/', methods=['GET'])
def index():
    readAudio('teste', {
    "words": [
        {
            "endTime": "1.700s",
            "startTime": "0.800s",
            "word": "Renan"
        },
        {
            "endTime": "2s",
            "startTime": "1.700s",
            "word": "Tô"
        },
        {
            "endTime": "3s",
            "startTime": "4.700s",
            "word": "fazendo"
        }
    ]
    },
    "Renan Tô fazendo",
    "TESTE", 
    "13/07/2020")
    send_email("renan.biagiotti22@gmail.com", "ApneaSleep - Relatorio.pdf")
    return "Audio analysis API"

@app.route('/analyseAudio', methods=['POST'])
@check_for_token
def analyseAudio():
    try:
        encodedAudio = request.json['encodedAudio']
        audioId = request.json['audioId']
        audioName = request.json['audioName']
        token = request.args.get('token')
        tokenJson = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        username = tokenJson.get('sub')

    except Exception as e:
        print("Erro :", e)
        return jsonify({'errorMessage':e}), 400
        
    return analyseAudioController(encodedAudio, audioId, username, audioName)

@app.route('/read', methods=['GET'])
def generatePDF():
    if (not request.json) and (not request.json['audioId']):
        abort(400)
    
    audioId = request.json['audioId']
    audioName = request.json['audioName']
    words = request.json['words']
    speech = request.json['speech']
    audioDate = request.json['informationDate']

    token = request.args.get('token')
    tokenJson = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    username = tokenJson.get('sub')

    return readAudio("", words, speech, audioName, audioDate)

if __name__ == '__main__':
    app.run(debug=True)
