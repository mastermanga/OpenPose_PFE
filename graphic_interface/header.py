# coding: utf-8
from tkinter import *

# Import functions.py
import functions


def header():
    header = Tk()
    header.title("Simulateur : Gardien de hocket sur gazon")

    menubar = Menu(header)

    menu = Menu(menubar, tearoff=0)

    # TODO
    menu.add_command(label="Voir les vidéos et analyses", command='#TODO')
    menu.add_command(label="Lancer une simulation", command=functions.avant_simulation)
    menubar.add_cascade(label="Naviguer", menu=menu)

    header.config(menu=menubar)

    return header
