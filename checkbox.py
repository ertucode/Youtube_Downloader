import tkinter
import customtkinter
from dataclasses import dataclass


@dataclass
class Checkbox:
    root: object
    id: str
    width: int
    state: str = "on"
    title : str = ""
    showing: bool = False
    type: str = "c"
    locx: int = 0
    locy: int = 0

    def __post_init__(self):
        self.idd = self.id if self.type == "b" else self.id + " - "+ self.title
        while len(self.idd) < self.width:
            self.idd += " "
        self.var = tkinter.StringVar()

    def packBox(self):
        try:
            self.checkbox
        except:
            self.checkbox = customtkinter.CTkCheckBox(master=self.root, text= self.idd, variable=self.var, 
                                                    offvalue="off", onvalue="on",command=self.checkbox_event)
        if self.state == "on":
            self.checkbox.select()
        if self.state == "off":
            self.checkbox.deselect()
        if self.type == "c":
            # expand = True,
            self.checkbox.pack( pady=5, padx = 10)
        elif self.type == "b":
            self.checkbox.place(relx=self.locx, rely=self.locy, anchor="nw")
        self.showing = True


    def changeColor(self,color):
        try:
            self.checkbox
        except:
            self.checkbox = customtkinter.CTkCheckBox(master=self.root, text= self.idd, variable=self.var, 
                                                    offvalue="off", onvalue="on",command=self.checkbox_event)
        self.checkbox.configure(text_color = color)
        

    def hide(self):
        if self.showing:
            try:
                self.checkbox.pack_forget()
                self.showing = False
            except:
                pass
                print("not instantiated")

    def checkbox_event(self):
        self.state = self.checkbox.get()

    def check(self):
        self.state = "on"
        self.checkbox.select()
        if self.id == "Subtitle":
            pass

    def decheck(self):
        self.state = "off"
        self.checkbox.deselect()
