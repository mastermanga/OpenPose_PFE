from functools import partial
from tkinter import *
import os


def lancer_simulation(spinbox, box):
    try:
        nb_run = str(spinbox.get())
        box.destroy()
        os.system('python ../record/record.py --runs ' + nb_run)
    except IndexError:
        print("No file selected")


def avant_simulation(window):
    window.withdraw()
    box = Toplevel(master=window)
    box.title("Lancer une simulation")
    box.geometry("325x90")
    label = Label(box, text="Combien d'attaques voulez-vous lancer ?")
    spinbox = Spinbox(box, from_=1, to=10, width=2)
    btn = Button(box, text="Lancer", command=lambda: [lancer_simulation(spinbox, box), window.deiconify()])

    label.pack(side=TOP)
    spinbox.pack()
    btn.pack(side=BOTTOM, padx=80, pady=5)
