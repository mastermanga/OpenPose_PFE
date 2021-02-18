from functools import partial
from tkinter import *
import os
import sys
import cv2


def lancer_simulation(spinbox, box):
    try:
        nb_run = str(spinbox.get())
        # box.destroy()
        os.system('python ./record/recordV2.py --runs ' + nb_run)
    except IndexError:
        print("No file selected")


def on_closing(box, window):
    window.deiconify()
    box.destroy()


def avant_simulation(window):
    window.withdraw()
    box = Toplevel(master=window)
    box.title("Lancer une simulation")
    box.geometry("325x90")
    box.protocol('WM_DELETE_WINDOW', partial(on_closing, box, window))
    label = Label(box, text="Combien d'attaques voulez-vous lancer ?")
    spinbox = Spinbox(box, from_=1, to=10, width=2)
    btn_lancer = Button(box, text="Lancer", command=partial(lancer_simulation, spinbox, box))
    btn_pre = Button(box, text="Revenir à l'accueil", command=partial(on_closing, box, window))

    label.pack(side=TOP)
    spinbox.pack()
    btn_lancer.pack(side=LEFT, padx=15, pady=5)
    btn_pre.pack(side=RIGHT, padx=15, pady=5)
    
def open_video(video_path):
    if sys.platform in ("linux", "linux2"):
        os.system("xdg-open " + video_path)
    elif sys.platform == "win32":
        video_path = video_path.replace('/', '\\')
        os.system("start " + video_path)
    elif sys.platform == "darwin":
        os.system("open " + video_path)
    else:
        print("platform not supported")
        
def get_frame(video_filename): 
    video = cv2.VideoCapture(video_filename)
    
    return video.read()

def image_to_thumbs(img):
    height, width, channels = img.shape
    thumbs = {"original": img}
    sizes = [640, 320, 160]
    for size in sizes:
        if (width >= size):
            r = (size + 0.0) / width
            max_size = (size, int(height * r))
            thumbs[str(size)] = cv2.resize(img, max_size, interpolation=cv2.INTER_AREA)
    return thumbs

def write_thumbs(video_path):
    image = get_frame(video_path)
    thumbs = image_to_thumbs(image[1])

    try:
        os.mkdir("./videos/mp4/02-01-2021/thumbs")
    except:
        pass

    for t in thumbs:
        cv2.imwrite("./videos/mp4/02-01-2021/thumbs/" + t + ".png", thumbs[t])
