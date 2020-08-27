import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import librosa as lr
from glob import glob
import base64
from matplotlib.backends.backend_pdf import PdfPages
from pdfFile import generatePDF
import boto3
from botocore.client import Config

def readAudio(audioBytes, words, speech, audioName, audioDate):

    # print(len(audio_files))
    try:

        audio, sfreq = lr.load(audioBytes, sr=44100)
        totalTime = lr.get_duration(y=audio, sr=sfreq)
    
        # print("audio file : ", audio_files[4])

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
        plt.xticks(size = 12)
        plt.yticks(size = 12)
        ax.set_ylabel("Amplitude do Som", fontsize=15)
        ax.set_xlabel("Tempo(s)", fontsize=15)
        
        with PdfPages('audioGraf.pdf') as pdf:
            F = plt.gcf()
            Size = F.get_size_inches()
            F.set_size_inches(8.5, 11, forward=True)
            plt.title("Gráfico do Audio", fontdict={'fontsize': 25, 'fontweight': 'bold'})
            pdf.savefig()

        generatePDF(time, audio, max(audio), list(time)[list(audio).index(max(audio))], min(audio), list(time)[list(audio).index(min(audio))], totalTime, words, speech, audioName, audioDate)

    except Exception as e:
        print("Analysis Error:",e)
        return "Erro ao realizar análise do Audio"