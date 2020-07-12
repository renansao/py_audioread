import base64
import os

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
        
        wav_file = open(path, "wb")
        decode_string = base64.b64decode(encodedAudio)
        wav_file.write(decode_string)

        return audioPath, path
    except Exception as e:
        print(e)
        return "Falha ao converter Base 64"