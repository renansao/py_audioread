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


@app.route('/oi', methods=['GET'])
@check_for_token
def index():
    return "Audio analysis API"

@app.route('/analyseAudio', methods=['POST'])
@check_for_token
def analyseAudio():
    try:
        encodedAudio = request.json['encodedAudio']
        audioId = request.json['audioId']

        token = request.args.get('token')
        tokenJson = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        username = tokenJson.get('sub')

        

    except:
        return jsonify({'errorMessage':'Erro ao analisar o audio'}), 400

    return analyseAudioService(encodedAudio, audioId, username)




@app.route('/convertToFile', methods=['POST'])
def conversor():
    if (not request.json) and (not request.json['base64']):
        abort(400)
    base64 = request.json['base64']
    #converted = conversorB64toFile(base64)
    converted = True
    if converted:
        return "Succesfully converted to file"
    else:
        return "An error occurred"

@app.route('/transformToText', methods=['GET'])
def transform():
    transformedText = transformToText()
    return transformedText

@app.route('/read', methods=['GET'])
def read():
    data_dir = 'audio_file'
    audio_files = glob(data_dir + '/*.wav')
    return readAudio(audio_files)

#TESTE PARA MOSTRAR O PSOT
@app.route('/brisa', methods=['POST'])
def get_test():
    tasks = [
        {
            'id': 1,
            'title': u'Buy groceries',
            'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
            'done': False
        },
        {
            'id': 2,
            'title': u'Learn Python',
            'description': u'Need to find a good Python tutorial on the web', 
            'done': False
        }
    ]
    if not request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

if __name__ == '__main__':
    app.run(debug=True)