from View import *
import os
from tkinter import filedialog
from pydub import AudioSegment
import mutagen.id3
from mutagen.easyid3 import EasyID3
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt

x = 0


def load_file(self):
    self.file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.mp3;*.aac")])
    if self.file_path:
        self.file = os.path.basename(self.file_path)
        update_info_label(self)

    self.file = cleaning(self.file_path, self.file)

    global data, sampleRate, t, dataInDbHigh, dataInDbMid, dataInDbLow, maxIndexHigh, maxIndexMid, maxIndexLow, maxLess5IndexHigh, maxLess5IndexMid, maxLess5IndexLow, maxLess25IndexHigh, maxLess25IndexMid, maxLess25IndexLow
    sampleRate, data = wavfile.read(self.file)
    print(f"sample rate = {sampleRate}Hz")
    self.length = round(data.shape[0] / sampleRate, 2)
    print(f"length = {self.length}s")
    update_length_label(self)
    dominantFrequency = np.array(data).max()
    self.selectedFrequency = dominantFrequency
    print(f"dominant frequency is {dominantFrequency}Hz")
    update_high_label(self)

    n = len(data)
    k = np.arange(n)
    T = n / sampleRate
    frq = k / T
    frq = frq[:len(frq) // 2]
    Y = np.fft.fft(data) / n
    Y = Y[:n // 2]

    plt.yscale("symlog")
    plt.plot(frq, abs(Y))
    plt.xlim(0, 1500)
    plt.xlabel("Freq (Hz)")
    plt.ylabel("Power")
    plt.title("Frequency vs Power")
    show_plt(plt)

    plt.plot(data)
    plt.ylabel("Amplitude")
    plt.xlabel("Time")
    plt.title("Waveform")
    show_plt(plt)

    spectrum, freqs, t, im = plt.specgram(data, Fs=sampleRate,
                                          NFFT=1024, cmap=plt.get_cmap('autumn_r'))
    plt.clf()
    plt.title("High RT60")
    plt.ylabel("Power (dB)")
    plt.xlabel("Time (s)")

    self.selectedFrequency = freqs[(np.abs(freqs - 10000)).argmin()]

    print("selected = " + str(self.selectedFrequency))
    selectedIndexHigh = np.where(np.array(freqs) == self.selectedFrequency)[0][0]
    print("selected index = " + str(selectedIndexHigh))
    dataInDbHigh = 10 * np.log10(spectrum[selectedIndexHigh])
    plt.plot(t, dataInDbHigh, linewidth=1, alpha=0.7, color="#004bc6")

    maxIndexHigh = np.argmax(dataInDbHigh)
    maxHigh = dataInDbHigh[maxIndexHigh]
    print("max = " + str(maxHigh))
    print("max index = " + str(maxIndexHigh))
    plt.plot(t[maxIndexHigh], dataInDbHigh[maxIndexHigh], "go")

    slicedArrayHigh = dataInDbHigh[maxIndexHigh:]
    maxLess5High = maxHigh - 5
    maxLess5High = slicedArrayHigh[(np.abs(slicedArrayHigh - maxLess5High)).argmin()]
    print("max less 5 = " + str(maxLess5High))
    maxLess5IndexHigh = np.where(dataInDbHigh == maxLess5High)
    print("max less 5 index = " + str(maxLess5IndexHigh))
    plt.plot(t[maxLess5IndexHigh], dataInDbHigh[maxLess5IndexHigh], "yo")

    maxLess25High = maxHigh - 25
    maxLess25High = slicedArrayHigh[(np.abs(slicedArrayHigh - maxLess25High)).argmin()]
    print("max less 25 = " + str(maxLess25High))
    maxLess25IndexHigh = np.where(np.array(dataInDbHigh) == maxLess25High)
    print("max less 25 index = " + str(maxLess25IndexHigh))
    plt.plot(t[maxLess25IndexHigh], dataInDbHigh[maxLess25IndexHigh], "ro")

    rt20High = (t[maxLess5IndexHigh] - t[maxLess25IndexHigh])[0]
    print(f"rt20 = {rt20High}")
    rt60High = 3 * rt20High
    rt60High = round(abs(rt60High), 2)
    plt.xlim(0, (rt60High * 1.5))
    plt.grid()
    show_plt(plt)

    self.highRT60 = rt60High
    update_high_RT60_label(self)

    print(f"The RT60 reverb time at freq {int(self.selectedFrequency)}Hz is {rt60High} seconds")

    plt.title("Mid RT60")
    plt.ylabel("Power (dB)")
    plt.xlabel("Time (s)")

    self.selectedFrequency = freqs[(np.abs(freqs - 1000)).argmin()]

    print("selected = " + str(self.selectedFrequency))
    selectedIndexMid = np.where(np.array(freqs) == self.selectedFrequency)[0][0]
    print("selected index = " + str(selectedIndexMid))
    dataInDbMid = 10 * np.log10(spectrum[selectedIndexMid])
    plt.plot(t, dataInDbMid, linewidth=1, alpha=0.7, color="#309600")

    maxIndexMid = np.argmax(dataInDbMid)
    maxMid = dataInDbMid[maxIndexMid]
    print("max = " + str(maxMid))
    print("max index = " + str(maxIndexMid))
    plt.plot(t[maxIndexMid], dataInDbMid[maxIndexMid], "go")

    slicedArrayMid = dataInDbMid[maxIndexMid:]
    maxLess5Mid = maxMid - 5
    maxLess5Mid = slicedArrayMid[(np.abs(slicedArrayMid - maxLess5Mid)).argmin()]
    print("max less 5 = " + str(maxLess5Mid))
    maxLess5IndexMid = np.where(dataInDbMid == maxLess5Mid)
    print("max less 5 index = " + str(maxLess5IndexMid))
    plt.plot(t[maxLess5IndexMid], dataInDbMid[maxLess5IndexMid], "yo")

    maxLess25Mid = maxMid - 25
    maxLess25Mid = slicedArrayMid[(np.abs(slicedArrayMid - maxLess25Mid)).argmin()]
    print("max less 25 = " + str(maxLess25Mid))
    maxLess25IndexMid = np.where(np.array(dataInDbMid) == maxLess25Mid)
    print("max less 25 index = " + str(maxLess25IndexMid))
    plt.plot(t[maxLess25IndexMid], dataInDbMid[maxLess25IndexMid], "ro")

    rt20Mid = (t[maxLess5IndexMid] - t[maxLess25IndexMid])[0]
    print(f"rt20 = {rt20Mid}")
    rt60Mid = 3 * rt20Mid
    rt60Mid = round(abs(rt60Mid), 2)
    plt.xlim(0, (rt60Mid * 1.5))
    plt.grid()
    show_plt(plt)

    self.midRT60 = rt60Mid
    update_mid_RT60_label(self)

    print(f"The RT60 reverb time at freq {int(self.selectedFrequency)}Hz is {rt60Mid} seconds")

    plt.title("Low RT60")
    plt.ylabel("Power (dB)")
    plt.xlabel("Time (s)")

    self.selectedFrequency = freqs[(np.abs(freqs - 250)).argmin()]

    print("selected = " + str(self.selectedFrequency))
    selectedIndexLow = np.where(np.array(freqs) == self.selectedFrequency)[0][0]
    print("selected index = " + str(selectedIndexLow))
    dataInDbLow = 10 * np.log10(spectrum[selectedIndexLow])
    plt.plot(t, dataInDbLow, linewidth=1, alpha=0.7, color="#fa0025")

    maxIndexLow = np.argmax(dataInDbLow)
    maxLow = dataInDbLow[maxIndexLow]
    print("max = " + str(maxLow))
    print("max index = " + str(maxIndexLow))
    plt.plot(t[maxIndexLow], dataInDbLow[maxIndexLow], "go")

    slicedArrayLow = dataInDbLow[maxIndexLow:]
    maxLess5Low = maxLow - 5
    maxLess5Low = slicedArrayLow[(np.abs(slicedArrayLow - maxLess5Low)).argmin()]
    print("max less 5 = " + str(maxLess5Low))
    maxLess5IndexLow = np.where(dataInDbLow == maxLess5Low)
    print("max less 5 index = " + str(maxLess5IndexLow))
    plt.plot(t[maxLess5IndexLow], dataInDbLow[maxLess5IndexLow], "yo")

    maxLess25Low = maxLow - 25
    maxLess25Low = slicedArrayLow[(np.abs(slicedArrayLow - maxLess25Low)).argmin()]
    print("max less 25 = " + str(maxLess25Low))
    maxLess25IndexLow = np.where(np.array(dataInDbLow) == maxLess25Low)
    print("max less 25 index = " + str(maxLess25IndexLow))
    plt.plot(t[maxLess25IndexLow], dataInDbLow[maxLess25IndexLow], "ro")

    rt20Low = (t[maxLess5IndexLow] - t[maxLess25IndexLow])[0]
    print(f"rt20 = {rt20Low}")
    rt60Low = 3 * rt20Low
    rt60Low = round(abs(rt60Low), 2)
    plt.xlim(0, (rt60Low * 1.5))
    plt.grid()
    show_plt(plt)

    self.lowRT60 = rt60Low
    update_low_RT60_label(self)

    print(f"The RT60 reverb time at freq {int(self.selectedFrequency)}Hz is {rt60Mid} seconds")

    average = (self.highRT60 + self.midRT60 + self.lowRT60)/3
    self.difference = round(average - 0.5, 2)
    update_difference_label(self)

    self.spectragram_button['state'] = 'normal'
    self.switch_button['state'] = 'normal'
    self.combine_button['state'] = 'normal'


def cleaning(file_path, file):
    index = 0
    while file[index] != '.':
        index += 1

    fileName = file[:index]
    fileExtension = file[index:]

    if fileExtension == ".wav":
        file = file_path
    elif fileExtension == ".mp3":
        AudioSegment.from_mp3(file_path).export(fileName + ".wav", format="wav")
        file = fileName + ".wav"
    elif fileExtension == ".flv":
        AudioSegment.from_flv(file_path).export(fileName + ".wav", format="wav")
        file = fileName + ".wav"
    elif fileExtension == ".ogg":
        AudioSegment.from_ogg(file_path).export(fileName + ".wav", format="wav")
        file = fileName + ".wav"

    rawAudio = AudioSegment.from_file(file, format="wav")
    channelCount = rawAudio.channels
    print(f"channel count = {channelCount}")

    if channelCount > 1:
        rawAudio.set_channels(1).export(fileName + "_mono.wav", format="wav")
        file = fileName + "_mono.wav"
        monoWavAudio = AudioSegment.from_file(file, format="wav")
        print(f"new channel count = {monoWavAudio.channels}")

    try:
        meta = EasyID3(file)
    except mutagen.id3.ID3NoHeaderError:
        return file
    meta["title"] = ""
    meta["version"] = ""
    meta["artist"] = ""
    meta["albumartist"] = ""
    meta["album"] = ""
    meta["date"] = ""
    meta["tracknumber"] = ""
    meta["genre"] = ""
    meta.save()

    return file


def spectragram():
    spectrum, freqs, t, im = plt.specgram(data, Fs=sampleRate,
                                          NFFT=1024, cmap=plt.get_cmap('autumn_r'))
    cbar = plt.colorbar(im)
    plt.title("Spectragram")
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    cbar.set_label("Intensity (dB)")
    show_plt(plt)


def switch(self):
    global x
    plt.ylabel("Power (dB)")
    plt.xlabel("Time (s)")

    if x == 0:
        plt.title("High RT60")

        plt.plot(t, dataInDbHigh, linewidth=1, alpha=0.7, color="#004bc6")
        plt.plot(t[maxIndexHigh], dataInDbHigh[maxIndexHigh], "go")
        plt.plot(t[maxLess5IndexHigh], dataInDbHigh[maxLess5IndexHigh], "yo")
        plt.plot(t[maxLess25IndexHigh], dataInDbHigh[maxLess25IndexHigh], "ro")

        plt.xlim(0, (self.highRT60 * 1.5))
        x += 1
    elif x == 1:
        plt.title("Mid RT60")

        plt.plot(t, dataInDbMid, linewidth=1, alpha=0.7, color="#309600")
        plt.plot(t[maxIndexMid], dataInDbMid[maxIndexMid], "go")
        plt.plot(t[maxLess5IndexMid], dataInDbMid[maxLess5IndexMid], "yo")
        plt.plot(t[maxLess25IndexMid], dataInDbMid[maxLess25IndexMid], "ro")

        plt.xlim(0, (self.midRT60 * 1.5))
        x += 1
    elif x == 2:
        plt.title("Low RT60")

        plt.plot(t, dataInDbLow, linewidth=1, alpha=0.7, color="#fa0025")
        plt.plot(t[maxIndexLow], dataInDbLow[maxIndexLow], "go")
        plt.plot(t[maxLess5IndexLow], dataInDbLow[maxLess5IndexLow], "yo")
        plt.plot(t[maxLess25IndexLow], dataInDbLow[maxLess25IndexLow], "ro")

        plt.xlim(0, (self.lowRT60 * 1.5))
        x = 0

    plt.grid()
    show_plt(plt)


def combine():
    plt.title("Combined RT60")
    plt.ylabel("Power (dB)")
    plt.xlabel("Time (s)")

    plt.plot(t, dataInDbHigh, linewidth=1, alpha=0.7, color="#004bc6")
    plt.plot(t, dataInDbMid, linewidth=1, alpha=0.7, color="#309600")
    plt.plot(t, dataInDbLow, linewidth=1, alpha=0.7, color="#fa0025")

    plt.plot(t[maxIndexHigh], dataInDbHigh[maxIndexHigh], "bo")
    plt.plot(t[maxIndexMid], dataInDbMid[maxIndexMid], "go")
    plt.plot(t[maxIndexLow], dataInDbLow[maxIndexLow], "ro")

    plt.plot(t[maxLess5IndexHigh], dataInDbHigh[maxLess5IndexHigh], "bo")
    plt.plot(t[maxLess5IndexMid], dataInDbMid[maxLess5IndexMid], "go")
    plt.plot(t[maxLess5IndexLow], dataInDbLow[maxLess5IndexLow], "ro")

    plt.plot(t[maxLess25IndexHigh], dataInDbHigh[maxLess25IndexHigh], "bo")
    plt.plot(t[maxLess25IndexMid], dataInDbMid[maxLess25IndexMid], "go")
    plt.plot(t[maxLess25IndexLow], dataInDbLow[maxLess25IndexLow], "ro")

    plt.legend(["High", "Mid", "Low"], loc="right")
    plt.grid()
    show_plt(plt)
