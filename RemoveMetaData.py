import mutagen.id3
from mutagen.easyid3 import EasyID3


def removeMetaData(filePath):
    try:
        file = EasyID3(filePath)
    except mutagen.id3.ID3NoHeaderError:
        exit()
    file["title"] = ""
    file["version"] = ""
    file["artist"] = ""
    file["albumartist"] = ""
    file["album"] = ""
    file["date"] = ""
    file["tracknumber"] = ""
    file["genre"] = ""
    file.save()
