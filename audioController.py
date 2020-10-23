from audioService import saveAudioToS3, analiseSpeech
from readAudio import readAudio
import datetime
import requests
from flask import jsonify
import json

#Method will receive the encodedAudio, audioId and username from the request,
#and will save the audio to its converted form (.WAV) in S3, after that, the
#audio will be analyzed and the application will try to define if the user did
#speak. After all of this, the application will generate a PDF, with all the data
#gathered from the audio sent. and save to S3.
def analyseAudioController(encodedAudio, audioId, username, audioName):

    try:
        #Save converted audio (.WAV) to S3 container.
        wavAudio, audioKey = saveAudioToS3(encodedAudio, username, audioId, audioName)

        #Analyse the possible speech and return a JSON String
        analysisResult, hasSpoken = analiseSpeech(wavAudio)

        if hasSpoken == True:
            wordsSpoken = []
            transcript = ""
            for i in range(len(analysisResult['results'])):
                wordsSpoken += analysisResult['results'][i]['alternatives'][0]['words']
                print("i=", i)
                transcript += analysisResult['results'][i]['alternatives'][0]['transcript'] + ". "
            print("wordsSpoken>: ", wordsSpoken)
            print("transcript>: ", transcript)
        else:
            wordsSpoken = [{'startTime': '', 'endTime': '', 'word': ''}]
            transcript = ''
            print("wordsSpoken>: ", wordsSpoken)
            print("transcript>: ", transcript)

        #Generate PDF with audio details
        pdfKey = readAudio(wavAudio,
        wordsSpoken,
        transcript,
        audioName,
        str((datetime.datetime.now()).strftime("%x")),
        username,
        audioId)

        #Call JAVA API to save S3 file keys
        #payload = {'audioId': audioId, 'pdfKey': pdfKey, 'audioKey': audioKey}
        
    except Exception as e:
        print("Error in service: ", e)
        return jsonify({'errorMessage':e}), 400

    return analysisResult