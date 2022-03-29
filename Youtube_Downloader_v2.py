import sys
import time
import traceback
#    except:
# traceback.print_exc()

# print(sys.argv[0])
# print("adsjf")
# print(sys.argv)

given = False

try:
    given = sys.argv[1]
    print(f"Input: {given}")
except:
    pass

def ps(text,t = 1.3):
    print(text)
    time.sleep(t)

def warn():
    import winsound
    frequency = 238  # Set Frequency To 2500 Hertz
    duration = 300  # Set Duration To 1000 ms == 1 second

    while frequency > 0 :
        winsound.Beep(frequency, duration)
        frequency -= 100
        duration -= 100
if given:

    t1 = given
    if t1[-1]=="/": t1 = t1[:-1]
    t2 = t1[8:]
    lan = video = audio = single = playlist = sub = False
    splits = t2.split(",")  
    url = splits[0]
    options = splits[1]

    if options[0] == "P":
        type = "p"
    elif options[0] == "S":
        type = "s"

    options1 = options[3:]
    options2 = options1.split("_")

    if "Video" in options2: video=True
    if "Audio" in options2: audio=True
    if "Subtitle" in options2: 
        sub = True
        lan = options2[-1]
    print(f"Url: {url}")  
    print(f"Type: {'Single' if type == 's' else 'Playlist'} - Video: {video} - Audio: {audio} - Subtitle: {sub} - Language: {lan}")
    print("")



from pytube import YouTube, Playlist
import os
import keyboard
# import pygame

# pygame.init()
# WIDTH, HEIGHT = 1000, 500
# WHITE = (255,255,255)
# win = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Youtube Downloader")
# mainfont = "berlinsansfbdemikalın"

# def draw(win,text):
#     win.fill(WHITE)
#     printText(win,WIDTH/2,HEIGHT/2,text)
#     pygame.display.update()

# def printText(win,x,y,text,font=mainfont,fontsize=15,color=(0,0,0)):
#     pos = (x,y)
#     myfont = pygame.font.SysFont(font,fontsize)
#     text_sur = myfont.render(text,True,color)
#     win.blit(text_sur,pos)

desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

def end():
    if keyboard.is_pressed("esc"):
        print("")
        print("Download cancelled..")
        sys.exit()

def downloadCallback(stream, file_handle, bytes_remaining):
    fileSize = stream.filesize
    bytes_downloaded = fileSize - bytes_remaining
    percentage = round((bytes_downloaded / fileSize) * 100, 2)
    mb = bytes_downloaded * 10**-6
    print(f" {percentage}% - {mb:.2f} MB - {stream.title}", end="\r")
    end()
    


            
def best_audio(streams):
    audios = streams.filter(only_audio=True)
    bestQ = 0
    for audio in audios:
        abr = ""
        for letter in audio.abr:
            if letter.isdigit():
                abr += letter
        abr = int(abr)
        if abr > bestQ:
            bestQ = abr
            best = audio
    return best

# def best_video(streams):
#     videos = streams.filter(only_video=True)
#     bestQ = 0
#     for video in videos:
#         resolution = ""
#         for letter in video.resolution:
#             if letter.isdigit():
#                 resolution += letter
#         resolution = int(resolution)
#         if resolution > bestQ:
#             bestQ = resolution
#             best = video
#     return best

def q(text):
    while text[-1] == ".":
        text = text[:-1]
    return text

def fixtitle(title):
    title = title.replace('"',"")
    title = title.replace("'","")
    return title


def downloadVideo(url,sub,lan=None,playlist=False,audio=False,video=False,willWait=False):
    
    end()
    yt = YouTube(url, on_progress_callback=downloadCallback)
    print(f"Downloading {yt.title}... Hold ESC to cancel")
    
    if playlist:
        ptitle = fixtitle(playlist.title)
    if not playlist:
        dir = f'{desktop}\\Youtube_Download'
    else:
        dir = f'{desktop}\\Youtube_Download\\{ptitle}'

    if not os.path.exists(dir):
        os.mkdir(dir)

    if video:
        best = yt.streams.filter(file_extension='mp4').filter(progressive=True).get_highest_resolution()
        best.download(output_path=dir)
        print(f"Downloaded video: {dir}/{best.title}.{best.subtype}")
    if audio:
        end()
        audio = best_audio(yt.streams)
        audio.download(output_path=dir)
        print(f"Downloaded audio: {dir}/{audio.title}.{audio.subtype}")

    if sub:
        end()
        vtitle = fixtitle(yt.title)
        if (yt.captions):
            picked = False
            while not picked:
                if lan in yt.captions:
                    caption = yt.captions[lan]
                    picked = True
                    text = caption.generate_srt_captions()
                    text = text.replace('\u266a',"")
                    try:
                        with open(f"{dir}\\{q(vtitle)}.txt", 'w') as f:
                            f.write(text)
                            print(f"Downloaded subtitle: {dir}/{vtitle}.txt")
                    except:
                        print("Subtitle has unsupported characters")
                elif "a."+lan in yt.captions:
                    caption = yt.captions["a."+lan]
                    picked = True
                    text = caption.generate_srt_captions()
                    text = text.replace('\u266a',"")
                    try:
                        with open(f"{dir}\\{q(vtitle)}.txt", 'w', encoding="utf-8") as f:
                            f.write(text)
                            print(f"Downloaded subtitle: {dir}/{vtitle}.txt")
                    except:
                        print("Subtitle has unsupported characters")
                else:
                    end()
                    print(f"Language not available for {vtitle}")
                    if willWait:
                        for caption in yt.captions:
                            print("Available languages: ")
                            print(caption.code)
                            lan = input("Language: (If you dont want subtitle enter no): ")
                            if lan == "no":
                                picked = True
                    else:
                        picked = True

        else:
            print("Subtitle not available")

def downloadPlaylist(url,sub,lan=None,audio=None,video=None,willWait=False):
    p = Playlist(url)
    counter = 0
    for url in p.video_urls:
        counter += 1
        print(f"Track count: {counter}")
        downloadVideo(url,sub,lan,p,audio,video,willWait=willWait)

import msvcrt, sys

def getInput(text,desiredoutputs):
    xd = None
    while not xd in desiredoutputs:
        xd = input(text)
        if xd in desiredoutputs:
            pass
        else:
            print('Invalid value')
            print("Press any key to continue.. ESC to exit..")
            key=msvcrt.getch()
            if(key == chr(27).encode()):
                sys.exit()
    return xd

if given:
    dealt = None
    match type:
        case "p" :
            yt = None
            try:
                yt = Playlist(url)
                xd = yt.title
                print(xd)
                downloadPlaylist(url,sub,lan=lan,audio=audio,video=video,willWait=False)
                warn()
                print("Downloads completed!!!")
            except Exception as error: 
                traceback.print_exc()
                if error == "SystemExit":
                    sys.exit()
                try:
                    yt = YouTube(url)
                except:
                    print('Invalid URL')
                    print("Press any key to continue.. ESC to exit..")
                    key=msvcrt.getch()
                    if(key == chr(27).encode()):
                        sys.exit()
                if yt:
                    type = "s" if getInput("You just gave a video link.. Do you want to download it? (y/n): ",["y","n"]) =="y" else "p"
                    if type == "s":dealt = True
        case "s":
            try:
                yt = YouTube(url)
                downloadVideo(url,sub,lan=lan,audio=audio,video=video,willWait=False)
                print("Downloads completed!!!")
            except Exception as error: 
                traceback.print_exc()
                if error == "SystemExit":
                    sys.exit()
                try:
                    yt = Playlist(url)
                    xd = yt.title
                except:
                    print('Invalid URL')
                    print("Press any key to continue.. ESC to exit..")
                    key=msvcrt.getch()
                    if(key == chr(27).encode()):
                        sys.exit()
                if yt:
                    type = "p" if getInput("You just gave a playlist link.. Do you want to download it? (y/n): ",["y","n"]) =="y" else "s"
                    if type == "p":dealt = True
    if dealt:
        match type:
            case "p" :
                downloadPlaylist(url,sub,lan=lan,audio=audio,video=video,willWait=False)
                warn()
                print("Downloads completed!!!")
            case "s" :
                downloadVideo(url,sub,lan=lan,audio=audio,video=video,willWait=False)
                print("Downloads completed!!!")

print("What do you want to download? ")
print("")
while True:
    
    type = getInput("p for playlist / s for singlefile = ",["s","p"])
    while True:
        try:
            url = input("Url = ")
            if type == "s":
                yt = YouTube(url)
            elif type == "p":
                yt = Playlist(url)
                xd = yt.title
            break
        except:
            print('Invalid URL')
            print("Press any key to continue.. ESC to exit..")
            key=msvcrt.getch()
            if(key == chr(27).encode()):
                sys.exit()

    video = audio = sub = "u"
    video = True if getInput("Video? (y/n): ",["y","n"]) == "y" else False
    audio = True if getInput("Audio? (y/n): ",["y","n"]) =="y" else False
    sub = True if getInput("Subtitles? (y/n): ",["y","n"]) =="y" else False

    willWait = False
    lan = None
    if sub:
        lan = input("Subtitle Language[tr for Turkish / en for English] = ")
        # willWait = True if getInput("Will you wait for subtitle questions or do you trust that the language will always be present(y/n): \n",["y","n"]) =="y" else False

    # type = "p"
    # url = "https://www.youtube.com/playlist?list=PLzxuWjRUOmNaRwzAo4V8vhx66uPslWsue"
    # audio = True
    # video = True
    # sub = True 
    # lan = "en"

    match type:
        case "p" :
            downloadPlaylist(url,sub,lan=lan,audio=audio,video=video,willWait=willWait)
            warn()
        case "s":
            downloadVideo(url,sub,lan=lan,audio=audio,video=video,willWait=willWait)
    print("Downloads completed!!!")
    
    end()