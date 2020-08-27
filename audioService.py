import base64
import io
from pydub import AudioSegment
from s3Utils import saveFileS3
import speech_recognition as sr
import json
from flask import jsonify
from s3Utils import retrieveS3File

#Given encodedAudio and id's, save converted audio file to S3 bucket
def saveAudioToS3(encodedAudio, username, audioId):

    try:
        #Generate Audio Key (name for S3)
        audioKey = generateAudioKey(username, audioId, ".wav")

        #Create M4A file base on B64 received in the request
        decodedAudio = base64.b64decode(encodedAudio)
        audioFile = io.BytesIO(decodedAudio)

        #Create BytesIO to convert M4A File to WAV file
        wav = io.BytesIO()

        #Convert audio using pydub.AudioSegment
        ##Declare de audio on it's native format
        sound2 = AudioSegment.from_file(audioFile, "m4a")
        ##Convert it to other available format
        sound2.export(wav, format="wav")

        #Call method to save audio file to S3
        #saveFileS3("apneasleepbucket", audioKey, wav.getvalue())
        
        #Close Buffer
        audioFile.close()

        #Return wav
        return wav
    
    except Exception as e:
        print(e)
        print("Error: ", e)
        return jsonify({'errorMessage':str(e)}), 400

#Given BytesIO of WAV audio, transform it to a transcipt of words, using googles API.
def analiseSpeech(audioWav):
    
    #Instanciate speech recogntion module
    r = sr.Recognizer()

    #Retrieve google credentials from S3 and put in a string
    credentials_json = retrieveS3File("apneasleepbucket", "googleCredentials/ApenaSleep-c58f74b11fb6.json")
    credentialsStr = credentials_json['Body']._raw_stream.data.decode()

    try:
        #Get wav audio bytes and instaciate a AudioData Object
        audio = sr.AudioData(audioWav.getvalue(), 44100, 4)
        
        print("Convertendo Audio para Texto ..... ")

        #Call Google Cloud API to try to find a speech on it
        result = r.recognize_google_cloud(audio,credentials_json=credentialsStr,language="pt-BR",show_all=True)
        
        #Return JSON string of the speech analysis result
        return result
    
    except Exception as e:
        print(e)
        print("Error: ", e)
        return jsonify({'errorMessage':str(e)}), 400


#Generate Audio Key (name for S3)
def generateAudioKey(username, audioId, extension):

    key = "user/" + "audio" + "/" + username + "/" + audioId + extension
    return key