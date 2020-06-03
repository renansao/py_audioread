import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
import base64

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
