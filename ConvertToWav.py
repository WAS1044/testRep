from pydub import AudioSegment


def convertToWav(filePath):
    file = AudioSegment.from_mp3(filePath)
    file.export("newFile.wav", format="wav")
