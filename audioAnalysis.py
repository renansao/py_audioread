from conversorB64toFile import conversorB64toFile
from transformText import transformToText
from transformText import convertAudioFiles

def analyseAudioService(encodedAudio, audioId, username):

    try:
        audioPath, audioDir = conversorB64toFile(encodedAudio, audioId, username)
        convertAudioFiles(audioDir)
        speech = transformToText(audioPath)
    except Exception as e:
        print("Erro no service",e)
        return "Falha na analise do audio"

    return speech