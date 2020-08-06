import base64
import os
import io
from pydub import AudioSegment
import boto3

#Retrieve ACCESS KEYS from enviroment
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

#Set S3 Configuration
s3 = boto3.resource(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

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
    sound2 = AudioSegment.from_file(audioFile, "m4a")
    sound2.export(wav, format="wav")

    #Search all buckets in account
    for bucket in s3.buckets.all():
        #Save audio (.WAV) in the container with the unique generated name
        bucket.put_object(Key=audioKey, Body=wav.getvalue())
    
    #Close Buffers
    wav.close()
    audioFile.close()

    return

#Generate Audio Key (name for S3)
def generateAudioKey(username, audioId, extension):

    key = "user/" + "audio" + "/" + username + "/" + audioId + extension
    return key