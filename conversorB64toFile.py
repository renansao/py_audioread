import base64
import os
import io
from pydub import AudioSegment
import boto3

def conversorB64toFile(encodedAudio, audioId, username):

    audioName = audioId + ".m4a"
    path = "audio_file/"+ username
    audioPath = "audio_file/"+ username + "/" + audioName

    try:
        os.open
        try:
            os.mkdir(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)
        
        wav_file = open(audioPath, "wb")
        decodedAudio = base64.b64decode(encodedAudio)
        wav_file.write(decodedAudio)

        return audioPath, path
    except Exception as e:
        print(e)
        return "Falha ao converter Base 64"

def convertEncodedAudioToBytes(encodedAudio):

    decodedAudio = base64.b64decode(encodedAudio)
    audioFile = io.BytesIO(decodedAudio)

    f = open("audio_file/testeee22.m4a", "wb")
    f.write(audioFile.getbuffer())
    f.close()

    return audioFile

def convertM4AToWavBytes(m4aBytes):
    try:
        sound = AudioSegment.from_raw("audio_file/testeee22.m4a")
        sound.export("audio_file/testeee2222.wav", format="wav")

        sound2 = AudioSegment.from_file("audio_file/testeee22.m4a", "m4a")
        sound2.export("audio_file/testeee3333.wav", format="wav")

    except Exception as e:
        print("Erro no service",e)
        return "Falha na analise do audio"

    return "yes"
