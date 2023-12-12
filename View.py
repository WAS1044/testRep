def update_info_label(self):
    self.info_label.config(text="File Loaded: " + self.file)


def update_length_label(self):
    self.length_label.config(text=f"Length = {self.length}s")


def update_high_label(self):
    self.high_label.config(text=f"Highest resonance = {self.selectedFrequency}Hz")


def update_high_RT60_label(self):
    self.highRT60_label.config(text=f"High RT60 = {round(self.highRT60, 2)}s")


def update_mid_RT60_label(self):
    self.midRT60_label.config(text=f"Mid RT60 = {round(self.midRT60, 2)}s")


def update_low_RT60_label(self):
    self.lowRT60_label.config(text=f"Low RT60 = {round(self.lowRT60, 2)}s")


def update_difference_label(self):
    self.difference_label.config(text=f"Difference = {self.difference}s")


def show_plt(plt):
    plt.show()
