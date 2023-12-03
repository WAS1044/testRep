from RemoveMetaData import *
from ConvertToWav import *

if __name__ == '__main__':
    file = input("Please enter the name of the audio file: ")
    removeMetaData(file)
    convertToWav(file)
