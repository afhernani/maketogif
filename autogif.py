#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import configparser
import os
from tkinter import filedialog, messagebox
from ToolTip import *
from movie import Movie
from utility import items_only_a
import time

__autor__ = 'Hernani Aleman Ferraz'
__email__ = 'afhernani@gmail.com'
__apply__ = 'Auto-Make-gif'
__version__ = 1.0

class GuiMovieToGif(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Auto Make gif from movies: ")
        self.geometry("650x300")
        self.protocol('WM_DELETE_WINDOW', self.confirmExit)
        self.datos = {}
        self.chimgvar = tk.IntVar()
        self.toplayout = tk.LabelFrame(self)
        self.search_button = tk.Button(self.toplayout, text='...', command=self.search_directory)
        self.make_button = tk.Button(self.toplayout, text='Make', command=self.make_gif)
        dirpath = os.path.abspath(os.path.split(os.path.abspath(__file__))[0])
        self._apply = tk.PhotoImage(file=os.path.join(dirpath, 'Images/logo.png'))
        self.wm_iconphoto(True, self._apply)
        self.dirpathmovies = tk.StringVar(value=dirpath)
        print(self.dirpathmovies.get())
        self.entrydirmovies = tk.Entry(self.toplayout, textvar=self.dirpathmovies)

        self.entrydirmovies.pack(side=tk.LEFT, fill=tk.X, expand=1)

        self.make_button.pack(side=tk.RIGHT)
        self.search_button.pack(side=tk.RIGHT)

        self.toplayout.pack(side=tk.TOP, fill=tk.X)

        self.box_list = tk.Listbox(self)
        self.box_list.pack(fill=tk.BOTH, expand=True)

        self.bottomlayout = tk.LabelFrame(self)

        self.chekbuttonimg = tk.Checkbutton(self.bottomlayout, text='img', variable=self.chimgvar,
                                            command=self.check_img)
        self.chekbuttonimg.select()
        createToolTip(self.chekbuttonimg, "select for remove files images")

        self.statusvalor = tk.StringVar(value="processing ...")
        self.status = tk.Label(self.bottomlayout, text="processing…", textvar=self.statusvalor, bd=1, anchor='w',
                               relief='sunken')  #

        self.chekbuttonimg.pack(side=tk.RIGHT)
        self.status.pack(side=tk.LEFT, fill=tk.X, expand=1)
        self.bottomlayout.pack(side='bottom', fill='x')

        # adicionamos utilidades con el raton y teclado para la lisbox.
        self.box_list.bind('<Double-Button-1>', self.double_button_box_list)
        self.box_list.bind('<ButtonRelease-1>', self.buttonrelease)
        self.box_list.bind("<Key>", self.presskey)
        self.box_list.focus_set()
        self.file_select = tk.StringVar()
        self.setingfile = 'autogif.ini'
        self.list_files_not_makegif = None
        self.list_files_further = None
        self.movie = None
        self.bind('<<food>>', self.next_movie)
        self.get_init_status()

    def next_movie(self, info):
        self.box_list.insert('end', self.movie.datos['file'])
        if len(self.list_files_not_makegif) > 0:
            # cogemos el 1 elemento que lo eliminamos de la lista.
            item = self.list_files_not_makegif.pop(0)
            self.file_select.set(os.path.join(self.dirpathmovies.get(), item))
            self.statusvalor.set('>> next_movie: ' + item + ' | len: '+ str(len(self.list_files_not_makegif)))
            self.update()
            time.sleep(5)
            try:
                self.movie = Movie(self.file_select.get(), bool(self.chimgvar.get()))
                self.movie.setwidget(self)
                print(self.movie)
                self.movie.run()
            except Exception as ex:
                print(ex)
        else:
            self.statusvalor.set('>> thread finished.')



    def check_img(self):
        print('variable check is', bool(self.chimgvar.get()))

    def get_init_status(self):
        '''
        extract init status of app
        Return:
        '''
        if not os.path.exists(self.setingfile):
            # inicializa la lista directorio actual
            return
        config = configparser.RawConfigParser()
        config.read(self.setingfile)
        dirpathmovies = config.get('Setings', 'dirpathmovies')
        if os.path.exists(dirpathmovies):
            self.dirpathmovies.set(dirpathmovies)
            # inicializa la lista con directorio duardao
     

    def set_init_status(self):
        '''
        write init status of app
        Return:
        '''
        config = configparser.RawConfigParser()
        config.add_section('Setings')
        config.set('Setings', 'dirpathmovies', self.dirpathmovies.get())
        with open(self.setingfile, 'w') as configfile:
            config.write(configfile)
        print('Write config file')

    def presskey(self, event):
        '''
         bind("<Key>", self.presskey)
         select item with keyboard Up / Down
        '''
        print('presskey ->', event)
        print('len = ', len(self.box_list.get(0, 'end')) - 1)
        w = event.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        print('valor =', value)
        iter = 0
        if event.keysym == 'Up' and index > 0:
            iter = index - 1
            self.box_list.selection_clear(index)
            self.box_list.selection_set(iter)
            self.selected_item_path(iter)
            print("selected ->", w.get(iter))
        if event.keysym == 'Down' and index < (len(self.box_list.get(0, 'end')) - 1):
            iter = index + 1
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

        """
        comprobar si existe el fichero adicionar o hacer algo para corregir
        la deficiencia -> perdida de la direccion path absoluta
        """
        # if not os.path.isdir(self.dirpathmovies.get()):
        #     dir = os.path.dirname(self.file_select.get())
        #     self.dirpathmovies.set(dir)
        # selected = os.path.join(self.dirpathmovies.get(), self.box_list.get(item))
        # self.statusvalor.set(os.path.abspath(selected))
        # self.file_select.set(self.statusvalor.get())

    def buttonrelease(self, event):
        '''
        seleccionar con el raton con un solo click
        '''
        print('buttonrelease ->', event)
        item = self.box_list.nearest(event.y)
        dato = self.box_list.get(item)
        print('valor =', dato)
        self.statusvalor.set(dato)

    def double_button_box_list(self, event):
        print('double_button_box_list')
        # if self.box_list.curselection():
        #     item = self.box_list.curselection()[0]
        #     file_name = self.box_list.get(item)
        #     print(file_name)
        #     # lo guardamos variable file_select y damos salida en la barra de estado.
        #     self.selected_item_path(item)
        #     '''
        #     thread = Thread(target=tarea, args=("ffplay " + "\"" + lb.get(file) + "\"",))
        #     thread.daemon = True
        #     thread.start()
        #     '''

    def search_directory(self):
        print('search directory instruction')
        self.statusvalor.set('select directory where are movies files to make gif')
        dirname = filedialog.askdirectory(initialdir=self.dirpathmovies.get(), title="Select directory")
        if not dirname == "":
            self.dirpathmovies.set(os.path.abspath(dirname))
            # self.init_listbox(os.path.abspath(dirname))

    def make_gif(self):
        print('make gif from list')
        self.statusvalor.set('make gif instruction')
        # if os.path.exists(self.file_select.get()):
        #     movie = Movie(self.file_select.get(), bool(self.chimgvar.get()))
        #     print(movie)
        #     movie.run()
        # else:
        #     return
        if not os.path.isdir(self.dirpathmovies.get()):
            return
        else:
            # limpiamos box_list
            self.box_list.delete(0, tk.END)
            # make directorio put thumbais
            working_file = os.path.join(self.dirpathmovies.get(), 'Thumbails')
            if not os.path.exists(working_file):
                os.mkdir(working_file)
            # make list objects
            self.crear_listas(self.dirpathmovies.get())
            # vamos a hacer el primero de la lista.
            if len(self.list_files_not_makegif) > 0:
                # cogemos el 1 elemento que lo eliminamos de la lista.
                item = self.list_files_not_makegif.pop(0)
                self.file_select.set(os.path.join(self.dirpathmovies.get(), item))
                self.statusvalor.set('>> next_movie: ' + item + ' | len: '+ str(len(self.list_files_not_makegif)))
                # print(self.file_select.get())
                try:
                    self.movie = Movie(self.file_select.get(), bool(self.chimgvar.get()))
                    self.movie.setwidget(self)
                    print(self.movie)
                    self.movie.run()
                except Exception as ex:
                    print(ex)
            else:
                self.statusvalor.set('>> anything to make: ' )


    def confirmExit(self):
        if messagebox.askokcancel('Quit', 'Are you sure you want to exit?'):
            self.set_init_status()
            self.destroy()
        print('end process')

    def init_listbox(self, search_dir):
        """ listar los ficheros en el directorio."""
        # borramos todos los elementos
        self.box_list.delete(0, tk.END)
        extensions = ('.mp4', '.MP4', '.avi', '.AVI', '.flv', '.FLV', '.mpg', '.MPG')
        for file in os.listdir(search_dir):
            if file.endswith(extensions):
                self.box_list.insert(0, file)
        self.box_list.selection_set(0)

    def crear_listas(self, search_dir):
        '''
        construye la lista de los ficheros sin sus imagenes
        en el directorio thrum base correspondiente.
        '''
        self.list_files_not_makegif, self.list_files_further = items_only_a(search_dir)


if __name__ == '__main__':
    print('init process: ')
    app = GuiMovieToGif()
    app.mainloop()
