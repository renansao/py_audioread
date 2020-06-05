from conversorB64toFile import conversorB64toFile
from transformText import transformToText

def analyseAudioService(encodedAudio, audioId, username):

    try:
        audioPath = conversorB64toFile(encodedAudio, audioId, username)
        speech = transformToText(audioPath)
    except Exception as e:
        print(e)

    return speech