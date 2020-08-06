import base64
import io
from pydub import AudioSegment
from s3Utils import saveFileS3

#Given encodedAudio and id's, save converted audio file to S3 bucket
def saveAudioToS3(encodedAudio, username, audioId):

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
    saveFileS3("apneasleepbucket", audioKey, wav.getvalue())
    
    #Close Buffers
    wav.close()
    audioFile.close()
    return

#Generate Audio Key (name for S3)
def generateAudioKey(username, audioId, extension):

    key = "user/" + "audio" + "/" + username + "/" + audioId + extension
    return key