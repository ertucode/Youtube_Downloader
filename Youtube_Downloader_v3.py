    # https://github.com/TomSchimansky/CustomTkinter/wiki
    # pip install -r filepath\requirements.txt
    # pip show modulename >>> Shows dependencies
    # pip freeze > requirements.txt


# --noconfirm --onedir --windowed --icon youtube.ico --add-data "c:\users\ertug\appdata\local\programs\python\python310\lib\site-packages\customtkinter;customtkinter\" "C:\Users\ertug\G_Drive\Code\Python\Youtube_Downloader_v3_venv\Youtube_Downloader_v3\Youtube_Downloader_v31.py"

# get python path, C:\Users\ertug\G_Drive\Code\Python\Youtube_Downloader_v3_venv\YoutubeVenv\Scripts\python.exe -m pip uninstall pyinstaller
# C:\Users\ertug\G_Drive\Code\Python\Youtube_Downloader_v3_venv\YoutubeVenv\Scripts\python.exe -m pip install pyinstaller
# C:\Users\ertug\G_Drive\Code\Python\Youtube_Downloader_v3_venv\YoutubeVenv\Scripts\pyinstaller.exe ........

# # Pyinstaller command
# cd ..\..\

# C:\Users\ertug\G_Drive\Code\Python\Youtube_Downloader_v3_venv\YoutubeVenv\Scripts\pyinstaller.exe --noconfirm --onedir --windowed --icon "C:/Users/ertug/G_Drive/Code/Python/Youtube_Downloader_v3_venv/Youtube_Downloader_v3/youtube.ico"  --upx-dir "C:/Users/ertug/G_Drive/Code/Python/upx-3.96-win64" --add-data "C:/Users/ertug/G_Drive/Code/Python/Youtube_Downloader_v3_venv/YoutubeVenv/Lib/site-packages/customtkinter;customtkinter/" --add-data "C:/Users/ertug/G_Drive/Code/Python/Youtube_Downloader_v3_venv/Youtube_Downloader_v3/youtube.ico;."  "C:/Users/ertug/G_Drive/Code/Python/Youtube_Downloader_v3_venv/Youtube_Downloader_v3/Youtube_Downloader_v3.py"

# --distpath C:\Users\ertug\G_Drive\Code\_MyApps --workpath C:\Users\ertug\G_Drive\Code\_MyApps\builds
# --workpath C:\Users\ertug\G_Drive\Code\_MyApps\builds

# C:/Users/ertug/G_Drive/Code/Python/Youtube_Downloader_v3_venv/YoutubeVenv/Scripts/pyinstaller.exe C:/Users/ertug/G_Drive/Code/Python/Youtube_Downloader_v3_venv/Youtube_Downloader_v3/Youtube_Downloader_v31.py


import tkinter
from tkinter import ttk
from configparser import ConfigParser

import customtkinter
import tkinter.font as tkfont
from tkinter import filedialog
from checkbox import Checkbox
from radio import RadioButton
from button import Button
from warnuser import WarnUser
from combobox import ComboBox

import sys
from pytube import YouTube, Playlist
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed




FRAME_BG_COLOR = "system3dDarkShadow"
BG_COLOR = "gray12"
COMPLETED_COLOR = "green yellow"

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

def round_up(n1,n2):
    """ Divide and round up"""
    return int(n1 / n2) + (n1 % n2 > 0)

def convert_to_win_path(title):
    """ Fix the title so it can be a Windows path"""
    chars = "\"\':<>/\\*?|"
    for c in chars:
        if c in title:
            title = title.replace(c,"_")
    if title:
        while title[-1] == ".":
            title = title[:-1]
    return title

def best_audio(streams):
    """ Pick the best audio from the stream"""
    audios = streams.filter(only_audio=True)
    bestQ = 0
    for audio in audios:
        abr = int("".join([letter for letter in audio.abr if letter.isdigit()]))
        if abr > bestQ:
            bestQ = abr
            best = audio
    return best


class App():
    """ Class for the whole app"""
    def __init__(self,given_type="s",url=""):
        """Inıtialize frames and if given input, check and apply them"""
        self.user_specified_directory = direct
        self.root = customtkinter.CTk()
        self.root.iconbitmap("youtube.ico")
        self.root.protocol("WM_DELETE_WINDOW", self.quit_me)
        self.root.resizable(False, False)
        self.type = given_type
        self.url = url
        self.WIDTH, self.HEIGHT = 1250, 500
        self.FULLHEIGHT = self.HEIGHT + 150
        self.center_window()
        self.root.title("Youtube Downloader v3")

        self.LIST_FRAME_X = 300
        self.LIST_FRAME_Y = self.HEIGHT * 0.05
        self.LIST_FRAME_WIDTH = self.WIDTH * 0.73
        self.LIST_FRAME_HEIGHT = self.HEIGHT * 0.7
        self.LIST_FRAME = customtkinter.CTkFrame(master=self.root,corner_radius= 10, fg_color = FRAME_BG_COLOR)
        self.LIST_FRAME.place(x = self.LIST_FRAME_X,y = self.LIST_FRAME_Y , width = self.LIST_FRAME_WIDTH, height = self.LIST_FRAME_HEIGHT)

        self.LEFT_FRAMEX = 50
        self.LEFT_FRAMEY = self.HEIGHT * 0.05
        self.LEFT_FRAME_WIDTH = 200
        self.LEFT_FRAME_HEIGHT = self.HEIGHT * 0.9
        self.LEFT_FRAME = customtkinter.CTkFrame(master=self.root,corner_radius=10,fg_color=FRAME_BG_COLOR)
        self.LEFT_FRAME.place(x = self.LEFT_FRAMEX,y= self.LEFT_FRAMEY , width = self.LEFT_FRAME_WIDTH , height = self.LEFT_FRAME_HEIGHT)

        self.RADIO_FRAME_Y = self.LIST_FRAME_Y + self.LIST_FRAME_HEIGHT + 0.030 * self.HEIGHT
        self.RADIO_FRAME_HEIGHT = 0.07 * self.HEIGHT
        self.RADIO_FRAME = customtkinter.CTkFrame(master=self.root,corner_radius= 10,fg_color=FRAME_BG_COLOR)
        self.RADIO_FRAME.place(x = self.LIST_FRAME_X,y = self.RADIO_FRAME_Y  , width = self.LIST_FRAME_WIDTH, height = self.RADIO_FRAME_HEIGHT)

        self.URL_FRAME_Y = self.RADIO_FRAME_Y + self.RADIO_FRAME_HEIGHT + self.HEIGHT * 0.01
        self.URL_FRAME_HEIGHT = self.HEIGHT * 0.1
        self.URL_FRAME = customtkinter.CTkFrame(master=self.root,corner_radius= 10,fg_color=FRAME_BG_COLOR)
        self.URL_FRAME.place(x = self.LIST_FRAME_X, y = self.URL_FRAME_Y, width = self.LIST_FRAME_WIDTH, height = self.URL_FRAME_HEIGHT)

        self.CONSOLE_FRAME_Y = self.URL_FRAME_Y + self.URL_FRAME_HEIGHT + 20
        self.CONSOLE_FRAME_HEIGHT = self.HEIGHT * 0.275
        self.CONSOLE_FRAME_WIDTH = self.WIDTH * 0.93
        self.CONSOLE_FRAME = customtkinter.CTkFrame(master=self.root,corner_radius= 10,fg_color=FRAME_BG_COLOR)
        self.CONSOLE_FRAME.place(x = self.LEFT_FRAMEX, y = self.CONSOLE_FRAME_Y, width = self.CONSOLE_FRAME_WIDTH, height = self.CONSOLE_FRAME_HEIGHT)

        self.apply_my_style()
        
        "Century Schoolbook","Cascadia Code","Rockwell Extra Bold"
        LIST_BOX_FONT = tkfont.Font(family="Cascadia Code", size = "9",weight="bold")
        self.list_box = tkinter.Listbox(self.CONSOLE_FRAME,font = LIST_BOX_FONT,fg = "gray84",bd = 0,bg =FRAME_BG_COLOR,width = 168,height = 8)
        ##come
        self.list_box.place(relx=-0.001, rely=-0.001, anchor="nw")
        self.STARTINGPOINT = 0
        self.playlist_radio_variable = tkinter.IntVar()
        self.playlist_radio_variable.set(self.STARTINGPOINT)   
        self.put_url_frame_items()
        self.change_layout()
        self.put_left_frame_items()

    def quit_me(self):
        """ Quit the program 
        Delay to make the bug less occuring
        """
        try:
            self.list_box.delete(0,'end')
            self.print_new_line("Closing..")
            self.list_box.itemconfig("end", {'fg': 'yellow'})
            self.root.update()
            time.sleep(1)
            self.root.destroy()
        except:
            print("excepting")
        
    def apply_my_style(self):
        """ Apply combobox and listbox styles"""
        style= ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground= FRAME_BG_COLOR, background= FRAME_BG_COLOR, foreground = "white", arrowcolor = "white",selectbackground="blue",lightcolor = FRAME_BG_COLOR)
        style.configure("TCombobox", bordercolor = "white")
        self.root.option_add('*TCombobox*Listbox.background', FRAME_BG_COLOR)
        self.root.option_add('*TCombobox*Listbox.foreground', "white")
        self.root.option_add('*TCombobox*Listbox.selectbackground', "dark slate gray")

    def change_directory(self):
        """ Change directory button pressed.. Check input and change directory if it is valid"""
        
        ## OLD WAY
        # def check_and_fix_directory(directory):
        #     directory = directory.replace("/","\\")
        #     directory = directory.replace("\\\\","\\")
            
        #     if len(directory.split("\\")) == 1:
        #         return False
        #     else:
        #         splits = directory.split("\\")
        #         root_path = splits[0].capitalize()
        #         folders = [convert_to_win_path(folder) for folder in splits[1:]]
        #         directory = root_path + "\\" + "\\".join(folders)   
        #         if os.path.exists(root_path + "\\"): 
        #             return directory
        #         else: return False

        # self.temp_directory = False
        # def create_change_directory_top_level():
        #     self.change_directory_root = customtkinter.CTkToplevel()
        #     self.change_directory_root.title("Change Directory")
        #     for i in range(4):
        #         self.change_directory_root.columnconfigure(i, weight=1)
        #     self.change_directory_root.rowconfigure(3, weight = 0)
            
        #     # self.change_directory_root_width = len(self.dir) * 10 if len(self.dir) * 10 > 400 else 400
        #     self.change_directory_root.resizable(False, False)
        #     self.change_directory_root_width = 400
        #     self.change_directory_root_height = 150
        #     self.center_window(self.change_directory_root,self.change_directory_root_width,self.change_directory_root_height)
        #     def ok_button_click_event(*args):
        #         self.temp_directory = self.directory_entry.get()
        #         if self.temp_directory == "default": 
        #             self.temp_directory = f"{os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')}\YouTube"
        #         self.temp_directory = check_and_fix_directory(self.temp_directory)
        #         if self.temp_directory: 
        #             self.change_directory_root.destroy()
        #             self.dir = self.temp_directory
        #         else:
        #             WarnUser("Invalid directory")
                    
        #     def cancel_button_click_event(*args):
        #         self.change_directory_root.destroy()

        #     self.change_directory_root.bind("<Return>", ok_button_click_event)
        #     self.change_directory_root.bind("<Escape>", cancel_button_click_event)
        #     # label = customtkinter.CTkLabel(master=self.change_directory_root, text="Change directory", width = self.width,text_font=("Cascadia Code",10))
        #     # label.grid(row = 1,column = 0 , pady = 5, columnspan = 2)
        #     but_width = 60
        #     ok_button = customtkinter.CTkButton(self.change_directory_root, text="OK", command=ok_button_click_event, width = but_width,text_font=("Cascadia Code",10))
        #     ok_button.grid(row = 2,column = 0, pady = 5)
        #     cancel_button = customtkinter.CTkButton(self.change_directory_root, text="CANCEL", command=cancel_button_click_event, width = but_width,text_font=("Cascadia Code",10))
        #     cancel_button.grid(row = 2,column = 3, pady = 5)
        #     self.directory_entry = customtkinter.CTkEntry(master=self.change_directory_root, placeholder_text=self.dir,width = self.change_directory_root_width * 0.95,text_font=("Cascadia Code",9))
        #     self.directory_entry.grid(row = 1,column = 0 , pady = 5, columnspan = 4)
            
        #     def set_directory(directory):
        #         self.directory_entry.delete(0,"end")
        #         if directory == "default":
        #             self.directory_entry.insert(0,f"{os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')}\YouTube")
        #         elif directory == "downloads":
        #             self.directory_entry.insert(0,f"{os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads')}")
        #         elif directory == "desktop":
        #             self.directory_entry.insert(0,f"{os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')}")
        #         elif directory == "current":
        #             self.directory_entry.insert(0,self.dir)

        #     current_button = customtkinter.CTkButton(self.change_directory_root, text="Current", command=lambda: set_directory("current"),text_font=("Cascadia Code",10))
        #     default_button = customtkinter.CTkButton(self.change_directory_root, text="Default", command=lambda: set_directory("default"),text_font=("Cascadia Code",10))
        #     downloads_button = customtkinter.CTkButton(self.change_directory_root, text="Downloads", command=lambda: set_directory("downloads"),text_font=("Cascadia Code",10))
        #     desktop_button = customtkinter.CTkButton(self.change_directory_root, text="Desktop", command=lambda: set_directory("desktop"),text_font=("Cascadia Code",10))

        #     current_button.grid(row=0,column=0,sticky="nw",padx = 5, pady = 15)
        #     default_button.grid(row=0,column=1,sticky="nw",padx = 5, pady = 15)
        #     downloads_button.grid(row=0,column=2,sticky="nw",padx = 5, pady = 15)
        #     desktop_button.grid(row=0,column=3,sticky="nw",padx = 5, pady = 15)
            
        # if self.temp_directory: self.dir = self.temp_directory
        # create_change_directory_top_level()

        # NEW WAY #
        self.temp_directory = filedialog.askdirectory(initialdir = self.user_specified_directory)

        if self.temp_directory:
            self.user_specified_directory = self.temp_directory

        parser = ConfigParser()
        parser.read(options_path)
        parser.set("directory","directory_path",self.user_specified_directory)
        with open(options_path,"w") as configfile:
            parser.write(configfile)

    def put_url_frame_items(self):
        """ Put url frame items"""
        self.change_url_button = Button(self.URL_FRAME,0.9,0.5,"Change Url",self.change_url,"coral1","red",150)
        self.url_entry = customtkinter.CTkEntry(master=self.URL_FRAME, placeholder_text="Enter URL",
                                        width = self.WIDTH * 0.4,text_font=("Cascadia Code",9))
        self.url_entry.pack(side = "left", padx = 8)
        self.url_entry.insert(0,self.url)

        self.type_radio_variable = tkinter.IntVar()
        self.URL_RADIO_BOX1 = RadioButton(self.URL_FRAME,0,1,sharedVar=[self.playlist_radio_variable,self.type_radio_variable],idd="Playlist")
        self.URL_RADIO_BOX2 = RadioButton(self.URL_FRAME,1,1,sharedVar=[self.playlist_radio_variable,self.type_radio_variable],idd="Single Track")   
        if self.type == "p" : self.type_radio_variable.set(0)
        else : self.type_radio_variable.set(1)

    def change_url(self):
        """ Change layout according to the url"""
        t = "p" if self.type_radio_variable.get() == 0 else "s"
        if self.url == self.url_entry.get() and self.type == t: return

        self.change_url_button.button.set_text("Processing...")
        self.change_url_button.button.configure(fg_color = "red", text_color = "white")
        self.change_url_button.button.state = "disabled"
        
        self.root.update()
        try:
            if self.type == "p":
                for lst in self.checkbox_list:
                    for box in lst:
                        del box
                self.checkbox_list = []
                for box in self.radioboxs:
                    del box
                self.radioboxs = []
                for child in self.LIST_FRAME.winfo_children():
                    if not type(child).__name__ == "CTkCanvas":
                        child.destroy() 
                for child in self.RADIO_FRAME.winfo_children():
                    if not type(child).__name__ == "CTkCanvas":
                        child.destroy()
            elif self.type == "s":
                for child in self.LIST_FRAME.winfo_children():
                    if not type(child).__name__ == "CTkCanvas":
                        child.destroy()
                
                del self.single_checkbox

        except Exception as e:  print(f"{e} + >>>Exception")


        self.url = self.url_entry.get()
        self.type = "p" if self.type_radio_variable.get() == 0 else "s"


        self.change_layout()

    def put_left_frame_items(self):
        """ Put left frame items"""
        self.SELECT_ALL_BUTTON= Button(self.LEFT_FRAME,0.5,0.05,"Select All Items",self.select_all_videos,"dark slate blue","purple1",width= 180)
        self.DESELECT_ALL_BUTTON = Button(self.LEFT_FRAME,0.5,0.12,"Deselect All Items",self.deselect_all_videos,"maroon","black",width= 180)
        self.SELECT_SHOWN_BUTTON = Button(self.LEFT_FRAME,0.5,0.19,"Select Shown Items",self.select_shown_videos,"dark slate blue","purple1",width= 180)
        self.DESELECT_SHOWN_BUTTON = Button(self.LEFT_FRAME,0.5,0.26,"Deselect Shown Items",self.deselect_shown_videos,"maroon","black",width= 180)
        


        self.vidbox = Checkbox(self.LEFT_FRAME, "Video", 100, "off",type = "b",locx = 0.25,locy = 0.32)
        self.vidbox.packBox()
        self.audbox = Checkbox(self.LEFT_FRAME, "Audio", 100, "off",type = "b",locx = 0.25,locy = 0.40)
        self.audbox.packBox()
        
        def Alltypes():
            """ All checkbox pressed """
            if self.allbox.var.get() == "off":
                self.vidbox.check()
                self.audbox.check()
                try:self.subbox.check();
                except:pass;
            elif self.allbox.var.get() == "on":
                self.vidbox.decheck()
                self.audbox.decheck()
                try:self.subbox.decheck()
                except:pass

        self.allbox = Checkbox(self.LEFT_FRAME, "All", 100, "off",type = "b",locx = 0.6,locy = 0.4)
        self.allbox.packBox()
        self.allbox.checkbox.configure(command = Alltypes) 
        self.download_button = Button(self.LEFT_FRAME,0.5,0.95,"Download",self.download_button_function,"grey16","grey30")
        self.change_dir_button = Button(self.LEFT_FRAME,0.5,0.85,"Change Directory",self.change_directory,"coral1","red")



    def check_if_url_agrees_with_type(self):
        """ Check if url agrees with type and warn if it does not"""
        self.url_is_playlist = False
        self.url_is_singlefile = False
        if not self.url == "" and not self.url == " ":
            if self.type == "p":
                try:
                    self.p = Playlist(self.url)
                    xd = self.p.title
                    self.url_is_playlist = True
                except:
                    try:
                        self.yt = YouTube(self.url,on_progress_callback=self.on_progress_download_callback,on_complete_callback=self.download_done_callback)
                        self.type = "s"
                        self.url_is_singlefile = True
                        WarnUser("You have given a single file link, But chosen playlist")
                    except:
                        WarnUser("Invalid URL")

            if self.type == "s":
                try:
                    self.yt = YouTube(self.url,on_progress_callback=self.on_progress_download_callback,on_complete_callback=self.download_done_callback)
                    self.url_is_singlefile = True
                except:
                    try:
                        p = Playlist(self.url)
                        xd = p.title
                        WarnUser("You have given a playlist link, But chosen single file")
                    except:
                        WarnUser("Invalid URL")

    def download_done_callback(self,downloaded_stream,download_path):
        """ Download done"""
        pass

    def change_layout(self):
        self.check_if_url_agrees_with_type()
        if self.url_is_playlist:
            self.get_titles_and_youtube_objects()
            self.video_count = len(self.titles)
            self.LIST_LENGTH = 10
            self.list_count = round_up(self.video_count,self.LIST_LENGTH)

            self.checkbox_list = []
            
            for j in range (0,self.list_count):
                # For boxes for a perticulator frame
                checkboxs = []
                for i in range(1,self.LIST_LENGTH + 1 ):   #This starts from 1 not 0!!!
                    if i+j*self.LIST_LENGTH > self.video_count: break
                    checkboxs.append(Checkbox(self.LIST_FRAME,f"{str(i+j*self.LIST_LENGTH)}", 400, title = self.titles[i+j*self.LIST_LENGTH-1]))
                self.checkbox_list.append(checkboxs)

            ############# INDIVIDUAL --- RADIOS ----- ####################            
            self.radioboxs = []
            for i in range(0,self.list_count):
                self.radioboxs.append(RadioButton(self.RADIO_FRAME,i,0,sharedVar=[self.playlist_radio_variable],boxes = self.checkbox_list))

            # Showing the first 10 items of the playlist
            for box in self.checkbox_list[self.STARTINGPOINT]:
                box.packBox()


        if self.url_is_singlefile:
            self.list_count = 1
            self.LIST_LENGTH = 10

            self.single_checkbox = Checkbox(self.LIST_FRAME,f"{str(1)}",400,title = self.yt.title)
            self.single_checkbox.packBox()

        if self.url_is_singlefile:
            if self.yt.captions:
                self.put_subtitle_frame_items()
            else:
                try:
                    for child in self.SUB_FRAME.winfo_children():
                        if not type(child).__name__ == "CTkCanvas":
                            child.destroy()
                except:
                    pass

        if self.url_is_playlist:
            self.put_subtitle_frame_items()

        
        self.change_url_button.button.set_text("Change Url")
        self.change_url_button.button.state = "normal"
        self.change_url_button.button.configure(fg_color = "coral1")
        self.change_url_button.button.configure(text_color = "white")
        self.root.update()

    def put_subtitle_frame_items(self):
        """ Update subtitle related items """
        self.SUB_FRAME = customtkinter.CTkFrame(master=self.LEFT_FRAME,corner_radius=10,fg_color=FRAME_BG_COLOR)
        self.SUB_FRAME.place(x = 0,y= self.LEFT_FRAME_HEIGHT * 0.48, width = self.LEFT_FRAME_WIDTH , height = self.LEFT_FRAME_HEIGHT / 3)
        self.subbox = Checkbox(self.SUB_FRAME, "Sub", 100, "off",type = "b",locx = 0.25,locy = 0.02)
        self.subbox.packBox()
        def give_advice():
            WarnUser("[tr] > Turkish, [en] > English, [a.lang] Auto Generated")

        self.sub_advice_button = Button(self.SUB_FRAME,0.1,0.1,"?",give_advice,"PaleGreen4","SpringGreen4",width = 30)

        captions = self.yt.captions if self.url_is_singlefile else self.YouTubes[0].captions
        self.sub_options = []
        for capt in captions:
            st = f"{capt}"
            sts = st.split('"')
            self.sub_options.append(sts[-2])
        if len(self.sub_options) == 0: self.sub_options.append("en")
        self.sub_options_combobox = ComboBox(self.SUB_FRAME,0.8,0.1,5,self.sub_options)

    def get_titles_and_youtube_objects(self):
        """ Get titles and youtube objects for playlist""" 
        self.titles = None

        if self.url_is_playlist:
            if self.type == "p":
                self.p = Playlist(self.url)
                self.urls = self.p.video_urls
                def get_youtube(url):
                        return YouTube(url,on_progress_callback = self.on_progress_download_callback,on_complete_callback=self.download_done_callback)
                        
                def get_title(ind,youtubeItem):
                        return (ind,youtubeItem.title)

                self.YouTubes = []
                for urll in self.urls:
                    self.YouTubes.append(get_youtube(urll))

                processes = []

                # YouTubes, url

                with ThreadPoolExecutor(max_workers=20) as executor:
                    for ind,youtubeItem in enumerate(self.YouTubes):
                        processes.append(executor.submit(lambda p: get_title(*p), (ind,youtubeItem)))


                NumberAndTitle = []
                for task in as_completed(processes):
                    NumberAndTitle.append(task.result())
                NumberAndTitle.sort()

                # NumberAndTitle = []
                # for ind,youtubeItem in enumerate(self.YouTubes):
                #     NumberAndTitle.append(get_title(ind,youtubeItem))

                self.titles = []
                for item in NumberAndTitle:
                    self.titles.append(item[1])
                if len(self.titles) > 210:
                    self.titles = self.titles[:210]
                    WarnUser("Can't put more than 210 videos")

        elif self.url_is_singlefile:
            pass

    def center_window(self,root=0,WIDTH=0,HEIGHT=0):
        """ Center Tk window"""
        w = WIDTH if WIDTH else self.WIDTH # width for the Tk root
        h = HEIGHT if HEIGHT else self.FULLHEIGHT # height for the Tk root

        # get screen width and height
        ws = root.winfo_screenwidth() if root else self.root.winfo_screenwidth() # width of the screen
        hs = root.winfo_screenheight() if root else self.root.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        # set the dimensions of the screen 
        # and where it is placed
        if root:
            root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        else:
            self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def print_new_line(self,text):
        """Print new line to the fake console"""
        self.list_box.insert("end"," "+ text)
        self.list_box.yview("end")
        self.root.update()

    def print_same_line(self,text):
        """Print to the same line in the fake console"""
        if self.list_box.get("end")[1] == " " or self.list_box.get("end")[1] == "-":
            self.list_box.delete("end")
        self.list_box.insert("end"," "+ text)
        self.list_box.yview("end")
        self.root.update()

    def on_progress_download_callback(self, stream, file_handle, bytes_remaining):
        fileSize = stream.filesize
        bytes_downloaded = fileSize - bytes_remaining
        percentage = round((bytes_downloaded / fileSize) * 100, 2)
        mbb = fileSize * 10**-6
        mb = bytes_downloaded * 10**-6

        self.video_progress_bar = customtkinter.CTkProgressBar(master=self.LEFT_FRAME,width = 100)
        self.video_progress_bar.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)
        self.video_progress_bar.set(percentage * 10**-2)
    
        self.print_same_line(f" {percentage}% - {mb:.2f} MB / {mbb:.2f} MB - {stream.title}")

    def select_all_videos(self):
        """ Select all videos in the playlist"""
        if self.url_is_playlist:
            for boxes in self.checkbox_list:
                for box in boxes:
                    box.state = "on"
                    if box.showing:
                        box.checkbox.select()

    def deselect_all_videos(self):
        """ Deselect all videos in the playlist """
        if self.url_is_playlist:
            for boxes in self.checkbox_list:
                for box in boxes:
                    box.state = "off"
                    if box.showing:
                        box.checkbox.deselect()

    def select_shown_videos(self):
        """ Select all videos that are visible in the playlist"""
        if self.url_is_playlist:
            for boxes in self.checkbox_list:
                for box in boxes:
                    if box.showing:
                        box.state = "on"
                        box.checkbox.select()

    def deselect_shown_videos(self):
        """ Deselect all videos that are visible in the playlist"""
        if self.url_is_playlist:
            for boxes in self.checkbox_list:
                for box in boxes:
                    if box.showing:
                        box.state = "off"
                        box.checkbox.deselect()

    def check_path(self):
        if self.url_is_playlist:
            ptitle = convert_to_win_path(self.p.title)
            self.download_directory = f'{self.user_specified_directory}\\{ptitle}'
        else:
            self.download_directory = self.user_specified_directory

    def download_button_function(self):
        """ Download desired items
            Disable buttons
            Show progress bars
        """
        self.check_path()
        if not os.path.exists(self.download_directory):
            os.mkdir(self.download_directory)

        if len(self.LIST_FRAME.winfo_children()) > 1:
            self.some_video_chosen = False
            self.download_button.button.set_text("Downloading...")
            self.download_button.button.state = "disabled"
            self.change_dir_button.button.state = "disabled"
            self.download_button.button.configure(fg_color = "light blue")
            self.download_button.button.configure(fg_color = "blue")
            self.change_url_button.button.configure(text_color = "white")
            self.list_box.delete(0,'end')
            # butterminate.button.configure(state=tkinter.DISABLED)
            self.download_button.button.configure(state=tkinter.DISABLED)

            self.audio = True if self.audbox.state == "on" else False
            self.video = True if self.vidbox.state == "on" else False
            try:self.sub = True if self.subbox.state == "on" else False
            except:self.sub = False
            if self.sub:
                self.lan = self.sub_options_combobox.combobox.get()
                self.lan = self.lan if len(self.lan) > 0 else "en"
            try:
                self.video_progress_bar.destroy()
            except:
                pass
            desired_item_count = 0
            if self.url_is_playlist:
                for boxes in self.checkbox_list:
                    for box in boxes:
                        if box.state == "on":
                            desired_item_count += 1
                        box.changeColor("white")
                if not desired_item_count == 1:
                    self.list_progress_bar = customtkinter.CTkProgressBar(master=self.LEFT_FRAME,width = 100)
                    self.list_progress_bar.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)
                    self.list_progress_bar.set(0)
                downloadedCount = 0
                add_playlist_info = True
                if self.audio or self.sub or self.video:
                    if add_playlist_info:
                        f = open(f"{self.user_specified_directory}\\{self.p.title}\\{self.p.title}.txt", 'w', encoding = "utf-8")
                        f.write(f"{self.p.title}\n")
                        f.write(f"{self.url}\n\n")
                    for boxes in self.checkbox_list:
                        for box in boxes:
                            if box.state == "on":
                                self.some_video_chosen = True
                                box.changeColor("sky blue")
                                self.yt = self.YouTubes[int(box.id)-1]
                                if add_playlist_info:
                                    try:
                                        f.write(f"{downloadedCount + 1} - {self.yt.title}\n")
                                    except Exception as err:
                                        print(err)
                                        f.write(f"{downloadedCount + 1} - Weird title\n")
                                self.download_file()
                                try:
                                    self.video_progress_bar.destroy()
                                except:
                                    pass 
                                if not desired_item_count == 1:
                                    downloadedCount += 1
                                    self.list_progress_bar.set(downloadedCount / desired_item_count)
                                box.changeColor(COMPLETED_COLOR)
                    if add_playlist_info:
                        f.close()

            elif self.url_is_singlefile:
                # self.singleCheckBox.changeColor(COMPLETEDCOLOR)
                if self.single_checkbox.state == "on":
                    self.some_video_chosen = True
                    if self.audio or self.sub or self.video:
                        downloadedCount = 1
                        self.download_file()
                        self.single_checkbox.changeColor(COMPLETED_COLOR)
                        try:
                            self.video_progress_bar.destroy()
                        except:
                            pass 
                            

            
            if self.audio or self.sub or self.video:
                if not downloadedCount == 0:
                    self.print_new_line("Downloads Completed..")
                    self.list_box.itemconfig("end", {'fg': 'yellow'})
            else:
                WarnUser("You have not chosen any file type")

            if not self.some_video_chosen:
                WarnUser("You have not chosen any videos")
                
            self.download_button.button.configure(state=tkinter.NORMAL)
            # butterminate.button.configure(state=tkinter.NORMAL)

            for child in self.LEFT_FRAME.winfo_children():
                if type(child).__name__ == "CTkProgressBar":
                    child.destroy()

            self.download_button.button.set_text("Download")
            self.download_button.button.state = "normal"
            self.download_button.button.configure(fg_color = "black")
            self.change_url_button.button.configure(text_color = "white")
            self.change_dir_button.button.state = "normal"
            self.download_button.button.configure(fg_color = "coral1")


    def download_file(self): 
        """ Download video, audio and subtitle"""
        self.print_new_line(f"Downloading - {self.yt.title} " + u"\u23e9" " Close Application to Cancel")

        if self.video:
            best = self.yt.streams.filter(file_extension='mp4').filter(progressive=True).get_highest_resolution()
            best.download(output_path=self.download_directory)
            # self.printNewLine(f"Downloaded video: {dir}/{best.title}.{best.subtype}")
            self.print_same_line("Video " + u"\u2714")
        if self.audio:
            audio = best_audio(self.yt.streams)
            audio.download(output_path=self.download_directory)
            self.print_same_line("Audio " + u"\u2714")
        if self.sub:
            vtitle = convert_to_win_path(self.yt.title)
            if (self.yt.captions):
                if self.lan in self.yt.captions:
                    self.download_sub(vtitle,self.lan)
                elif "a."+self.lan in self.yt.captions:
                    self.download_sub(vtitle,"a."+self.lan)
                else:
                    self.print_new_line("Subtitle" + u"\u2716" "Language not available")

            else:
                self.print_new_line("Subtitle not available")

    def download_sub(self,vtitle,lan):
        """Download subtitle of the desired language.. If its going to take too long, make a guess"""
        hours = self.yt.length / 60 / 60
        minutes = (hours % 1) * 60
        secs = ( minutes % 1) * 60
        cutoff = 9.5
        if (hours > cutoff):
            estimation_in_minutes = (1175 + (89.28571 - 1175)/(1 + (int(hours)/16.07373)**428.7844)) / 60
            self.print_new_line(f"-Downloading subtitle")
            self.print_new_line(f"-Vidoe length: {int(hours)}:{int(minutes)}:{int(secs)} - Estimated subtitle download time: {estimation_in_minutes} min")

        caption = self.yt.captions[lan]
        text = caption.generate_srt_captions()
        text = text.replace('\u266a',"")
        lines = text.split("\n")
        f = open(f"{self.download_directory}\\{vtitle}_{lan}.txt", 'w')  

        for i,line in enumerate(lines):
            try:
                f.write(f"{line}\n")
            except:
                f.write("Unsupported characters \n")
        if (hours > cutoff):
            self.list_box.delete("end")
        self.print_same_line("Subtitle " + u"\u2714")
        f.close()

if __name__ == "__main__":
    """ If there are download path options get them, else create options.ini"""
    parser = ConfigParser()
    options_dir = f"{(os.path.join(os.environ['USERPROFILE']))}\Cavit_options\\"
    options_path = options_dir+"youtube_options.ini"
    if not os.path.exists(options_path):
        if not os.path.exists(options_dir): os.makedirs(options_dir)
        with open(options_path, 'w') as f:
            f.write("[directory]\n") 
            f.write("directory_path = desktop\YouTube\n") 
            f.write("default = desktop\YouTube\n")

    parser.read(options_path)
    read_dir = parser.get("directory","directory_path")
    if read_dir == "desktop\YouTube":
        direct = f"{os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')}\YouTube"
    else:
        direct = read_dir

    """ If command is given, apply to the program"""
    given = False

    try:
        given = sys.argv[1]
    except:
        pass
    if given:

        t1 = given
        if t1[-1]=="/": t1 = t1[:-1]
        t2 = t1[8:]
        splits = t2.split(",")  
        url = splits[0]
        options = splits[1]

        if options[0] == "P":
            giventype = "p"
        elif options[0] == "S":
            giventype = "s"
    if given:
        app = App(giventype,url)
    else:
        app = App()
    app.root.mainloop()
    



    