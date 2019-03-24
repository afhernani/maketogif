#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import os

class GuiMovieToGif(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Make gif from movie: ")
        self.geometry("400x300")
        self.iconbitmap('Images/Kaleidoscope-alt.ico')
        self.protocol('WM_DELETE_WINDOW', self.confirmExit)
        self.toplayout = tk.LabelFrame(self)
        self.search_button=tk.Button(self.toplayout, text='...', command=self.search_directory)
        self.make_button= tk.Button(self.toplayout, text='Make', command=self.make_gif)

        self.dirpathmovies = tk.StringVar(value=os.path.split(os.path.abspath(__file__))[0])
        print(self.dirpathmovies.get())
        self.entrydirmovies= tk.Entry(self.toplayout, textvar=self.dirpathmovies)

        self.entrydirmovies.pack(side=tk.LEFT, fill=tk.X, expand=1)
        
        self.make_button.pack(side=tk.RIGHT)
        self.search_button.pack(side=tk.RIGHT)
        
        self.toplayout.pack(side=tk.TOP, fill=tk.X)
        
        self.box_list = tk.Listbox(self)
        self.box_list.pack(fill=tk.BOTH, expand=True)
        
        self.statusvalor = tk.StringVar(value="processing ...")
        self.status = tk.Label(self, text="processing…", textvar=self.statusvalor, bd=1, anchor='w', relief='sunken') # 
        self.status.pack(side='bottom', fill='x') 

    def search_directory(self):
        print('search directory instruction')
        self.statusvalor.set('select directory where are movies files to make gif')
        dirname = filedialog.askdirectory(initialdir=self.dirpathmovies.get(), title="Select directory")
        if not dirname=="":
            self.dirpathmovies.set(dirname)

    def make_gif(self):
        print('make gif instruction')
        self.statusvalor.set('make gif instruction')

    def confirmExit(self):
        if messagebox.askokcancel('Quit', 'Are you sure you want to exit?'):
            self.destroy()
            print('end process')


if __name__ == '__main__':
    
    print('init process: ')
    app = GuiMovieToGif()
    app.mainloop()