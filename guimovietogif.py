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
        #self.iconbitmap('Images/Kaleidoscope-alt.ico')
        self.iconbitmap('@Images/Business.xbm')
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

        # inicializa la lista.
        self.init_listbox(self.dirpathmovies.get())
        # adicionamos utilidades con el raton y teclado para la lisbox.
        self.box_list.bind('<Double-Button-1>', self.double_button_box_list)
        self.box_list.bind('<ButtonRelease-1>', self.buttonrelease)
        self.box_list.bind("<Key>", self.presskey)
        self.file_select = tk.StringVar();



    def presskey(self, event):
        print('presskey ->', event)
        print('len = ', len(self.box_list.get(0,'end'))-1)
        w=event.widget
        index = int(w.curselection()[0])
        value=w.get(index)
        print('valor =', value)
        iter = 0
        if event.keysym == 'Up' and index > 0:
            iter = index-1
            self.box_list.selection_clear(index)
            self.box_list.selection_set(iter)
            self.selected_item_path(iter)
            print("selected ->", w.get(iter))
        if event.keysym == 'Down' and index < (len(self.box_list.get(0,'end'))-1):
            iter = index+1
            self.box_list.selection_clear(index)
            self.box_list.selection_set(iter)
            self.selected_item_path(iter)
            print("selected ->", w.get(iter))
        
    def selected_item_path(self, item):
        '''
         item -> int elemento de la lista,
         localiza la direccion absoluta del fichero y asigna su cadena
         a la barra de estado y almacnea su valor ne la variable de file_select
        '''
        selected = os.path.join(self.dirpathmovies.get(), self.box_list.get(item))
        self.statusvalor.set(os.path.abspath(selected))
        self.file_select.set(self.statusvalor.get())

    def buttonrelease(self, event):
        '''
        seleccionar con el raton con un solo click
        '''
        print('buttonrelease ->', event)
        item = self.box_list.nearest(event.y)
        print('valor =', self.box_list.get(item))
        self.selected_item_path(item)
        

    def double_button_box_list(self, event):
        print('double_button_box_list')
        if self.box_list.curselection():
            item = self.box_list.curselection()[0]
            file_name = self.box_list.get(item)
            print(file_name)
            # lo guardamos variable file_select y damos salida en la barra de estado.
            self.selected_item_path(item)
            '''
            thread = Thread(target=tarea, args=("ffplay " + "\"" + lb.get(file) + "\"",))
            thread.daemon = True
            thread.start()
            '''

    def search_directory(self):
        print('search directory instruction')
        self.statusvalor.set('select directory where are movies files to make gif')
        dirname = filedialog.askdirectory(initialdir=self.dirpathmovies.get(), title="Select directory")
        if not dirname=="":
            self.dirpathmovies.set(dirname)
            self.init_listbox(dirname)

    def make_gif(self):
        print('make gif instruction')
        self.statusvalor.set('make gif instruction')

    def confirmExit(self):
        if messagebox.askokcancel('Quit', 'Are you sure you want to exit?'):
            self.destroy()
            print('end process')

    def init_listbox(self, search_dir):
        """ listar los ficheros en el directorio."""
        # borramos todos los elementos
        self.box_list.delete(0, tk.END)
        for file in os.listdir(search_dir):
            if file.endswith(".mp4"):
                self.box_list.insert(0, file)
            if file.endswith(".flv"):
                self.box_list.insert(tk.END, file)

if __name__ == '__main__':
    
    print('init process: ')
    app = GuiMovieToGif()
    app.mainloop()