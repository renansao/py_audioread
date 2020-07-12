from flask import Flask, jsonify
from flask import request
from flask import abort
from readAudio import readAudio
from glob import glob
from transformText import transformToText
from conversorB64toFile import conversorB64toFile
from functools import wraps
import jwt
from audioAnalysis import analyseAudioService
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = "RraIY0negneEQzv3XO6kwjN4XVtsul1A"

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
@check_for_token
def index():
    return "Audio analysis API"

@app.route('/analyseAudio', methods=['POST'])
@check_for_token
def analyseAudio():
    try:
        encodedAudio = request.json['encodedAudio']
        #print("Base64: ", encodedAudio)
        audioId = request.json['audioId']

        token = request.args.get('token')
        tokenJson = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        username = tokenJson.get('sub')

        

    except Exception as e:
        print("exp :", e)
        return jsonify({'errorMessage':e}), 400
        
    return analyseAudioService(encodedAudio, audioId, username)




@app.route('/convertToFile', methods=['POST'])
@check_for_token
def conversor():
    if (not request.json) and (not request.json['base64']):
        abort(400)
    
    base64 = request.json['base64']
    audioId = request.json['audioId']
    token = request.args.get('token')
    tokenJson = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    username = tokenJson.get('sub')
    
    converted = conversorB64toFile(base64, audioId, username)
    #converted = True
    if converted:
        return "Succesfully converted to file"
    else:
        return "An error occurred"

@app.route('/read', methods=['GET'])
def read():
    data_dir = 'audio_file'
    audio_files = glob(data_dir + '/*.wav')
    return readAudio(audio_files)

if __name__ == '__main__':
    app.run(debug=True)
