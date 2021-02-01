# coding: utf-8
from tkinter import *
from PIL import ImageTk, Image
import time
import os

fenetre = Tk()

lfBienvenue = LabelFrame(fenetre, text="Bienvenue", padx=10, pady=10)
lfBienvenue.pack(fill="both", expand="yes")
frameCnt = 36
frames = [PhotoImage(file='hocket.gif', format='gif -index %i' % (i)) for i in range(frameCnt)]


def update(ind):
    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    label.configure(image=frame)
    fenetre.after(100, update, ind)


label = Label(lfBienvenue)


Button(fenetre, text='Lancer', command=os.system("python ../record/record.py")).pack(side=LEFT, padx=80, pady=5)
Button(fenetre, text='Quitter', command=fenetre.quit).pack(side=RIGHT, padx=80, pady=5)

label.pack()

fenetre.after(0, update, 0)
fenetre.mainloop()
