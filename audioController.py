from audioService import saveAudioToS3

#Method will receive the encodedAudio, audioId and username from the request,
#and will save the audio to its converted form (.WAV) in S3, after that, the
#audio will be analyzed and the application will try to define if the user did
#speak. After all of this, the application will generate a PDF, with all the data
#gathered from the audio sent. and save to S3,
def analyseAudioController(encodedAudio, audioId, username):

    try:
        #Save converted audio (.WAV) to S3 container.
        saveAudioToS3(encodedAudio, username, audioId)

    except Exception as e:
        print("Error in service: ", e)
        return e

    return "speech"