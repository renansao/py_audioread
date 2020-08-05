import base64
import os
import io
from pydub import AudioSegment
import boto3

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

print(AWS_ACCESS_KEY_ID)
print(AWS_SECRET_ACCESS_KEY)

s3 = boto3.resource(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

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

    wav = io.BytesIO()
    sound2 = AudioSegment.from_file(audioFile, "m4a")
    sound2.export(wav, format="wav")

    for bucket in s3.buckets.all():
        bucket.put_object(Key="users/audiofileHEROKU.wav", Body=wav.getvalue())
        bucket.put_object(Key="users/audiofileHEROKU.m4a", Body=audioFile.getvalue())
    wav.close()
    audioFile.close()

    return "ok"

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
