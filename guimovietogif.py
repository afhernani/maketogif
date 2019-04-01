#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import os
import sys
import subprocess
import re
import io
import shutil
import configparser
import threading

thread = threading
bloquea = threading.Lock()
isthread = False

class GuiMovieToGif(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Make gif from movie: ")
        self.geometry("400x300")
        #self.iconbitmap('Images/Kaleidoscope-alt.ico')
        self.iconbitmap('@Images/Business.xbm')
        self.protocol('WM_DELETE_WINDOW', self.confirmExit)
        self.datos = {}
        self.toplayout = tk.LabelFrame(self)
        self.search_button=tk.Button(self.toplayout, text='...', command=self.search_directory)
        self.make_button= tk.Button(self.toplayout, text='Make', command=self.make_gif)
        dirpath = os.path.abspath(os.path.split(os.path.abspath(__file__))[0])
        self.dirpathmovies = tk.StringVar(value=dirpath)
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


        # adicionamos utilidades con el raton y teclado para la lisbox.
        self.box_list.bind('<Double-Button-1>', self.double_button_box_list)
        self.box_list.bind('<ButtonRelease-1>', self.buttonrelease)
        self.box_list.bind("<Key>", self.presskey)
        self.box_list.focus_set()
        self.file_select = tk.StringVar()
        self.setingfile = 'seting.ini'
        self.get_init_status()

    def get_init_status(self):
        '''
        extract init status of app
        Return:
        '''
        if not os.path.exists(self.setingfile):
            # inicializa la lista directorio actual
            self.init_listbox(self.dirpathmovies.get())
            return
        config= configparser.RawConfigParser()
        config.read(self.setingfile)
        dirpathmovies = config.get('Setings', 'dirpathmovies')
        if os.path.exists(dirpathmovies):
            self.dirpathmovies.set(dirpathmovies)
            # inicializa la lista con directorio duardao
            self.init_listbox(self.dirpathmovies.get())
        else:
            self.init_listbox(self.dirpathmovies.get())
        pass

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

        """
        comprobar si existe el fichero adicionar o hacer algo para corregir
        la deficiencia -> perdida de la direccion path absoluta
        """
        if not os.path.isdir(self.dirpathmovies.get()):
            dir = os.path.dirname(self.file_select.get())
            self.dirpathmovies.set(dir)
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
        if not dirname == "":
            self.dirpathmovies.set(os.path.abspath(dirname))
            self.init_listbox(os.path.abspath(dirname))

    def make_thread(self):
        global bloquea
        global isthread
        bloquea.acquire()
        if os.path.exists(self.file_select.get()):
            self.datos = self.info_from_video()
            print('datos video ->', self.datos)
            self.extract_frames(num=5)
            self.make_gif_f_frames()
            print('datos video ->', self.datos)
        bloquea.release()
        isthread = False

    def make_gif(self):
        print('make gif instruction')
        self.statusvalor.set('make gif instruction')
        global thread
        global isthread
        if isthread:
            print('>> thread is alive')
            return
        thread = threading.Thread(target=self.make_thread)
        thread.daemon = True
        thread.start()
        isthread = True

    def confirmExit(self):
        if messagebox.askokcancel('Quit', 'Are you sure you want to exit?'):
            self.set_init_status()
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
        self.box_list.selection_set(0)

    def printOutput(self, string):
        '''
        Pretty print multi-line string
        '''
        for line in string.splitlines():
            print('    >> {}'.format(line.decode('utf8')))

    def runCommand(self, command):
        p = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout
        while True and p:
            line = p.readline()
            if not line:
                break
            self.printOutput(line)

    def info_from_video(self):
        print('extrac_images_from_videos')
        video_info = {}
        video_info['movie'] = self.file_select.get()
        command = ['ffmpeg', '-i', video_info['movie']]

        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout, stderr = process.communicate()

            matches = re.search(b'Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),',
                                stdout, re.DOTALL).groupdict()
            if matches:
                t_hour = matches['hours']
                t_min = matches['minutes']
                t_sec = matches['seconds']

                t_hour_sec = int(t_hour) * 3600
                t_min_sec = int(t_min) * 60
                t_s_sec = float(t_sec)

                total_sec = t_hour_sec + t_min_sec + t_s_sec
                video_info['time']=total_sec
                print('hora, minuto, segundo:', t_hour, t_min, t_sec)
                print('total de segundos:', total_sec)

            # This matches1 is to get the frames por segundo
            matches1 = re.search(b'(?P<fps>(\d+.)* fps)', stdout)
            if matches1:
                print('fps ->', matches1['fps'])
                frame_rate = matches1['fps'].split(b' ')[0]
                video_info['fps'] = float(frame_rate)
                print('fps ->', float(frame_rate))

            matches2 = re.search(b' (?P<width>\d+)x(?P<heigh>\d{2,3}[, ])', stdout)
            if matches2:
                print(matches2)
                width = int(matches2['width'])
                heigh = int(matches2['heigh'].replace(b',',b' '))
                print('formato: ->', matches2, width, heigh)
                video_info['formato'] = [width, heigh]


            #averiaguar el ratio.
            matches3 = re.search(b'bitrate:\s{1}(?P<bitrate>\d+?)\s{1}', stdout)
            if matches3:
                print('matches3 ->', matches3['bitrate'])
                video_info['bitrate'] = int(matches3['bitrate'])

        except subprocess.CalledProcessError as e:
            print(e.output)

        return video_info

    def extract_frames(self, file=None, num=None):
        '''
        extract frames from file
        file = file asignated, num = number of frames extract video to the gif
        :return: None
        '''
        if not file:
            file = self.datos['movie']
        # obtener un nombre de fichero independiente del fichero y fichero de trabajo
        if not num:
            num = 1
        import uuid
        name = str(uuid.uuid4()) + '-%04d.png'
        self.datos['code_frame'] = name
        #working file:
        working_file = os.path.join(os.path.dirname(self.datos['movie']), 'Thumbails')
        self.datos['working_file'] = working_file
        if not os.path.exists(working_file):
            os.mkdir(working_file)
        # ficheros de frames de salida
        work_dir = os.path.join(working_file, name)
        #determinar los factores de la linea de comando.
        command = ['ffmpeg']
        valor = self.datos['time']
        if valor:
            valor = valor * 1000 / (num + 1)
        command.extend(['-ss', str(int(valor/1000)), '-i', file, '-vf', 'fps=1/' + str(int(valor/1000))
                           , '-vframes', str(num)
                           ,  work_dir, '-hide_banner'])
        print('Linea de comando ->', command)
        self.runCommand(command)
        print('end extract_frames')

    def make_gif_f_frames(self, framerate=1, scale='200:-1'):
        '''
        make a gif from cedec frame
        :return:
        '''
        name = self.datos['code_frame']
        working_file = self.datos['working_file']
        work_dir = os.path.join(working_file, name)
        command = ['ffmpeg', '-y', '-framerate', str(framerate), '-i', work_dir, '-vf', 'scale=' + scale ]
        self.datos['file']= os.path.split(self.datos['movie'])[-1]
        file_out = os.path.join(os.path.dirname(self.datos['movie']), 'Thumbails', self.datos['file'] + '_thumbs_0000.gif')
        command.extend([file_out])
        print('create gif command ->', command)
        self.runCommand(command)
        #vamos a borrar los ficheros de imagen
        code = name.split('-')[0]
        pattern = '^' + code
        mypath = self.datos['working_file']
        print('remove:')
        for root, dirs, files in os.walk(mypath):
            for file in filter(lambda x: re.match(pattern, x), files):
                print(file)
                os.remove(os.path.join(root, file))
        '''
        code.pop()
        refcode=''
        for item in code:
            refcode += item + '-'
        print('remove:')
        print(refcode + '*.png')
        import fnmatch
        for file in os.listdir(self.datos['working_file']):
            print(file)
            if fnmatch.fnmatch(file.upper(), refcode + '*.png'):
                print(file)
                os.remove(os.path.join(self.datos['working_file'], file))
        '''
        print('made_gif_f_frames')


if __name__ == '__main__':

    print('init process: ')
    app = GuiMovieToGif()
    app.mainloop()
