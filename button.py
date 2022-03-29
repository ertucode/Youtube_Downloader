import tkinter
import customtkinter
from dataclasses import dataclass
from typing import Callable
from dataclasses import dataclass, field


@dataclass
class Button:
    root: object
    locx : int
    locy : int
    text: str
    func : Callable
    color: str
    hcolor: str
    width: int = 150

    def __post_init__(self):
        self.button = customtkinter.CTkButton(master=self.root, text=self.text, command=self.func)
        self.button.configure(fg_color = self.color, hover_color = self.hcolor)
        if not self.width == 31:
            self.button.place(relx=self.locx, rely=self.locy, width=self.width, anchor=tkinter.CENTER)
        else:
            self.button.grid(row=1,column=2,rowspan=1)



