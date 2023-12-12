from Model import *
import tkinter as tk

dimensions = ""


class AudioGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Analyzer")
        self.root.geometry(dimensions)

        self.load_button = tk.Button(root, text="Load Audio File", command=lambda: load_file(self))
        self.load_button.pack(pady=10)

        self.info_label = tk.Label(root, text="")
        self.info_label.pack()

        self.length_label = tk.Label(root, text="")
        self.length_label.pack()

        self.high_label = tk.Label(root, text="")
        self.high_label.pack()

        self.highRT60_label = tk.Label(root, text="")
        self.highRT60_label.pack()

        self.midRT60_label = tk.Label(root, text="")
        self.midRT60_label.pack()

        self.lowRT60_label = tk.Label(root, text="")
        self.lowRT60_label.pack()

        self.difference_label = tk.Label(root, text="")
        self.difference_label.pack()

        self.spectragram_button = tk.Button(root, text="View Spectragram", command=spectragram)
        self.spectragram_button.pack(pady=10)
        self.spectragram_button['state'] = 'disabled'

        self.switch_button = tk.Button(root, text="Switch", command=lambda: switch(self))
        self.switch_button.pack(pady=10)
        self.switch_button['state'] = 'disabled'

        self.combine_button = tk.Button(root, text="Combine Figures", command=combine)
        self.combine_button.pack(pady=10)
        self.combine_button['state'] = 'disabled'

        self.file_path = ""
        self.file = ""
        self.length = 0
        self.selectedFrequency = 0
        self.highRT60 = 0
        self.midRT60 = 0
        self.lowRT60 = 0
        self.difference = 0


if __name__ == "__main__":
    with open("setup.cfg", "r") as file:
        line = file.readline()
        index = 0
        while line[index] != "[":
            index += 1

        command = line[index + 1:]

        index = 0
        while command[index] != "]":
            index += 1

        command = command[:index]

        if command == "window_size":
            index = 0
            while line[index] != "=":
                index += 1

            dimensions = line[index + 1:]

    root = tk.Tk()
    app = AudioGUI(root)
    root.mainloop()
