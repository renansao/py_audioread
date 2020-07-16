import speech_recognition as sr
from pydub import AudioSegment
import os
import argparse
from flask import jsonify
import json
import sys


def convertAudioFiles(audioDir):
    formats_to_convert = ['.m4a']
    for (dirpath, dirnames, filenames) in os.walk(audioDir):
        for filename in filenames:
            if filename.endswith(tuple(formats_to_convert)):

                filepath = dirpath + '/' + filename
                (path, file_extension) = os.path.splitext(filepath)
                file_extension_final = file_extension.replace('.', '')
                try:
                    track = AudioSegment.from_file(filepath,
                            file_extension_final)
                    wav_filename = filename.replace(file_extension_final, 'wav')
                    wav_path = dirpath + '/' + wav_filename
                    print('CONVERTING: ' + str(filepath))
                    file_handle = track.export(wav_path, format='wav')
                    print(filepath)
                    os.remove(filepath)
                except Exception as e:
                    print("ERROR CONVERTING " + str(filepath))
                    print(e)

def transformToText(audioPath):
    
    r = sr.Recognizer()

    audioPath = audioPath[:-4]
    audioPath = audioPath + ".wav"

    try:
        convertAudioFiles(audioPath)

        with sr.AudioFile(audioPath) as source:
            r.adjust_for_ambient_noise(source)
            audio = r.record(source)
            print("Convertendo Audio para Texto ..... ")
            
            with open(r"credentials.json", "r") as f:
                credentials_json = f.read()
                result = r.recognize_google_cloud(audio,credentials_json=credentials_json,language="pt-BR",show_all=True)
                words = result['results'][0]['alternatives'][0]['words']
                transformedText = result['results'][0]['alternatives'][0]['transcript']

            #transformedTextJson = json.dumps(transformedText)
            #alternativeJson = json.dumps((json.loads(transformedTextJson).get('alternative')))

            #confidence = json.loads(alternativeJson).get('confidence')
            #print('confidence = ', confidence)


            return (jsonify({"speech":transformedText, "words": words}))

            

    except Exception as e:
        print(e)
        print("Error: ", e)
        return jsonify({'errorMessage':str(e)}), 400
