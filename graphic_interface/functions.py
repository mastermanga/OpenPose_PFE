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
    btn_lancer = Button(box, text="Lancer", command=partial(lancer_simulation, spinbox, box))
    btn_pre = Button(box, text="Revenir à l'accueil", command=partial(on_closing, box, window))

    label.pack(side=TOP)
    spinbox.pack()
    btn_lancer.pack(side=LEFT, padx=15, pady=5)
    btn_pre.pack(side=RIGHT, padx=15, pady=5)
