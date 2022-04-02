import tkinter
from tkinter import ttk
from dataclasses import dataclass




@dataclass
class ComboBox:
    root: object
    x: int
    y: int
    width: int
    options: list
    #gives: list

    def __post_init__(self):
        self.combobox = ttk.Combobox(master=self.root, values=self.options, width=self.width)
        self.combobox.place(relx=self.x, rely=self.y, anchor=tkinter.CENTER)
        self.combobox.current(0)

    # def read(self):
    #     ind = self.options.index(self.combobox.get())
    #     return self.gives[ind]