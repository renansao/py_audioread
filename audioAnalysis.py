from conversorB64toFile import saveAudioToS3, conversorB64toFile, convertEncodedAudioToBytes, convertM4AToWavBytes
from transformText import transformToText
from transformText import convertAudioFiles

def analyseAudioService(encodedAudio, audioId, username):

    try:
        #audioPath, audioDir = conversorB64toFile(encodedAudio, audioId, username)
        #convertAudioFiles(audioDir)
        #speech = transformToText(audioPath)

        saveAudioToS3(encodedAudio, username, audioId)

        m4aAudioBytes = convertEncodedAudioToBytes(encodedAudio)
        #wavAudioBytes = convertM4AToWavBytes(m4aAudioBytes)
        print(m4aAudioBytes)

    except Exception as e:
        print("Erro no service: ", e)
        print(e.with_traceback())
        return e

    return "speech"