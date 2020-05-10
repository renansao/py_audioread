from flask import Flask, jsonify
from flask import request
from flask import abort
from readAudio import readAudio
from glob import glob
from transformText import transformToText

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return True

@app.route('/transformToText', methods=['GET'])
def transform():
    transformToText()
    return True


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