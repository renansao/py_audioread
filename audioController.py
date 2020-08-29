from audioService import saveAudioToS3, analiseSpeech
from readAudio import readAudio
import datetime


#Method will receive the encodedAudio, audioId and username from the request,
#and will save the audio to its converted form (.WAV) in S3, after that, the
#audio will be analyzed and the application will try to define if the user did
#speak. After all of this, the application will generate a PDF, with all the data
#gathered from the audio sent. and save to S3.
def analyseAudioController(encodedAudio, audioId, username, audioName):

    try:
        #Save converted audio (.WAV) to S3 container.
        wavAudio = saveAudioToS3(encodedAudio, username, audioId)

        #Analyse the possible speech and return a JSON String
        analysisResult = analiseSpeech(wavAudio)

        #Generate PDF with audio details
        readAudio(wavAudio,
        analysisResult['results'][0]['alternatives'][0]['words'],
        analysisResult['results'][0]['alternatives'][0]['transcript'],
        audioName,
        str((datetime.datetime.now()).strftime("%x")))

        #Call JAVA API to save
        

    except Exception as e:
        print("Error in service: ", e)
        return e

    return analysisResult