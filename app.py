'''
Project: Top Trumps Game
Author: Julia Hryn
'''
from tkinter import Tk, Label, Button, Frame
from logic import game_controller
from tkinter import *
from interface import main_menu

def main():
    screen = Tk()
    main_menu(screen)
    screen.mainloop()

if __name__ == '__main__':
    main()