import tkinter
import customtkinter
from dataclasses import dataclass
import time



@dataclass
class WarnUser:
    text: str

    def __post_init__(self):
        customtkinter.set_appearance_mode("dark")
        self.root = customtkinter.CTkToplevel()
        self.root.title("Help")
        self.width = len(self.text) * 10 if len(self.text) * 10 > 200 else 200
        self.center_window()
        def button_click_event():
            self.root.destroy()

        label = customtkinter.CTkLabel(master=self.root, text=self.text, width = self.width,text_font=("Cascadia Code",10))
        label.grid(row = 0,column = 0 , pady = 5)
        but_width = 120
        button = customtkinter.CTkButton(self.root, text="OK", command=button_click_event, width = but_width,text_font=("Cascadia Code",10))
        button.grid(row = 1,column = 0, pady = 5)

        

    def center_window(self):
        w = self.width # width for the Tk root
        h = 80 # height for the Tk root
        # get screen width and height
        ws = self.root.winfo_screenwidth() # width of the screen
        hs = self.root.winfo_screenheight() # height of the screen
        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        XOFFSET = 50
        YOFFSET = 20
        self.root.geometry('%dx%d+%d+%d' % (w, h, x + XOFFSET, y + YOFFSET)) # set the dimensions of the screen and where it is placed

