# coding: utf-8
from tkinter import *
# import tkinter as tk
from functools import partial
import functions
import display_app




def header():
    header = Tk()
    header.title("Simulateur : Gardien de hocket sur gazon")
    # header.geometry = ("500x500")

    # frame = Frame(header, highlightbackground="black", highlightthickness=1)
    # btn = Button(frame, text="Voir les vidéos et analyses", command=open_records)

    # frame.place(relheight=0.1, relwidth=1.0)

    # menubar = Menu(header)

    # menu = Menu(menubar, tearoff=0)

    # # TODO
    # menu.add_command(label="Voir les vidéos et analyses", command='#TODO')
    # menu.add_command(label="Lancer une simulation", command=functions.avant_simulation)
    # menubar.add_cascade(label="Naviguer", menu=menu)

    # header.config(menu=menubar)

    return header
