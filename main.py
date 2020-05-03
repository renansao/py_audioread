import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
import librosa as lr
import base64
import speech_recognition as sr
from pydub import AudioSegment
import os
import argparse


def main():
    data_dir = 'audio_file'
    audio_files = glob(data_dir + '/*.wav')
    # convertAudioFiles()
    readAudio(audio_files)
    transformToText(audio_files)


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

def readAudio(audio_files):

    print(len(audio_files))

    audio, sfreq = lr.load(audio_files[4]) 

    print("audio file : ", audio_files[4])

    time = np.arange(0,len(audio)) / sfreq

    print("Time: ", time)
    print("Audio: ", audio)
    print("Máxima amplitude: ", max(audio), ", Ocorre no tempo ", list(time)[list(audio).index(max(audio))])
    print("Minima amplitude: ", min(audio), ", Ocorre no tempo ", list(time)[list(audio).index(min(audio))])
    print(min(audio))

    print(len(time))
    print(len(audio))

    fig, ax = plt.subplots()
    ax.plot(time, audio)
    ax.set(xlabel="Tempo (s)", ylabel="Amplitude do Som")
    plt.show()


def transformToText(audio_files):
    sound = "audio_file/record19.wav"
    
    r = sr.Recognizer()

    with sr.AudioFile(sound) as source:
        r.adjust_for_ambient_noise(source)
        print("Converting Audio To Text ..... ")
        audio = r.listen(source)
    
    try:
        print("Converted Audio Is : \n" + r.recognize_google(audio, language = 'pt-PT'))

    except Exception as e:
        print(e)
        print("Error: ".format(e))



if __name__ == "__main__":
    main()