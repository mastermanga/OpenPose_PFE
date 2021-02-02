from functools import partial
from tkinter import *
import os


def lancer_simulation(nb_simulation):
    try:
        # os.system('python ../record/record.py --runs ' + str(nb_simulation))
        print('run : python ../record/record.py --runs ' + str(nb_simulation))
    except IndexError:
        print("No file selected")


def avant_simulation():
    box = Tk()
    box.title("Lancer une simulation")
    box.geometry("325x90")
    label = Label(box, text="Combien de vidéo de simulation voulez-vous lancer ?")
    spinbox = Spinbox(box, from_=1, to=10, width=2)
    # Ne prend que "1" en compte
    nb_simulation = spinbox.get()
    btn = Button(box, text="Lancer", command=partial(lancer_simulation, nb_simulation))

    label.pack(side=TOP)
    spinbox.pack()
    btn.pack(side=BOTTOM, padx=80, pady=5)
    box.mainloop()
