from conversorB64toFile import conversorB64toFile

def analyseAudioService(encodedAudio, audioId, username):

    audioFile = conversorB64toFile(encodedAudio, audioId, username)

    return username