import base64
import os

def conversorB64toFile(encodedAudio, audioId, username):

    audioName = audioId + ".wav"
    path = "audio_file/"+ username
    audioPath = "audio_file/"+ username + "/" + audioName
    #audioPath = "audio_file/" + audioName

    try:
        os.open
        try:
            os.mkdir(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)
        
        wav_file = open(audioPath, "wb")
        decode_string = base64.b64decode(encodedAudio)
        wav_file.write(decode_string)

        return True
    except:
        return False