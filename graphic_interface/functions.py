from functools import partial
from tkinter import *
import os
import sys
import cv2


def lancer_simulation(spinbox, box):
    try:
        nb_run = str(spinbox.get())
        # box.destroy()
        os.system('python ../record/recordV2.py --runs ' + nb_run)
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
    btn = Button(box, text="Lancer", command=partial(lancer_simulation, spinbox, box))

    label.pack(side=TOP)
    spinbox.pack()
    btn.pack(side=BOTTOM, padx=80, pady=5)
