import speech_recognition as sr
from pydub import AudioSegment
import os
import argparse
from flask import jsonify
import json
import sys
sys.path.append("/app/ffmpeg/bin")
import ffmpeg
AudioSegment.converter = "/app/ffmpeg/bin/ffmpeg.exe"
AudioSegment.ffmpeg = "/app/ffmpeg/bin/ffmpeg.exe"
AudioSegment.ffprobe = "/app/ffmpeg/bin/ffprobe.exe"

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
        
    
            # print(r.recognize_google(audio, language = 'pt-PT', show_all=True))
            ### Validar se iremos utilizar o show_all - o que ele faz, retorna todas as possibilidades que encontrou na leitura além da que o algoritimo achou "mais correta"
            #{'alternative': [{'transcript': 'mas é então deixa eu te falar consegui fazer um conversor aqui', 'confidence': 0.95794368},
            #{'transcript': 'mas é então deixa eu te falar conseguia fazer um conversor aqui'}, 
            #{'transcript': 'mas é então deixa eu te falar consegui fazer um conversor AC'}
            #{'transcript': 'Pois é então deixa eu te falar consegui fazer um conversor aqui'},
            #{'transcript': 'mas é então deixa eu te falar consegui fazer um conversor aqui ó'}],
            #'final': True}
            # a frase neste exemplo era: "mas é então deixa eu te falar consegui fazer um conversor aqui"

            print("Texto convertido : \n" + r.recognize_google(audio, language = 'pt-PT'))
            transformedText = r.recognize_google(audio, language = 'pt-PT')
            #r.recognize_bing()
            

            #transformedTextJson = json.dumps(transformedText)
            #alternativeJson = json.dumps((json.loads(transformedTextJson).get('alternative')))

            #confidence = json.loads(alternativeJson).get('confidence')
            #print('confidence = ', confidence)


            return jsonify({"speech":transformedText})

            

    except Exception as e:
        print(e)
        print("Error: ", e)
        return jsonify({'errorMessage':str(e)}), 400
