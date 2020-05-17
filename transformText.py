import speech_recognition as sr
from pydub import AudioSegment
import os
import argparse

def convertAudioFiles():
    formats_to_convert = ['.m4a']
    for (dirpath, dirnames, filenames) in os.walk("audio_file/"):
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
                    os.remove(filepath)
                except:
                    print("ERROR CONVERTING " + str(filepath))

def transformToText():
    sound = "audio_file/record19.wav"
    
    r = sr.Recognizer()

    with sr.AudioFile(sound) as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)
        print("Convertendo Audio para Texto ..... ")
    
    try:
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
        return transformedText

    except Exception as e:
        print(e)
        print("Error: ".format(e))
