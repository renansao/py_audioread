import base64

def conversorB64toFile(base64Text):
    # exemplo de base64 acima
    try:
        wav_file = open("audio_file/tempTeste.wav", "wb")
        decode_string = base64.b64decode(base64Text)
        wav_file.write(decode_string)
        return True
    except:
        return False