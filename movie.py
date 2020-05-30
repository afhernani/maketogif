#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import re
import subprocess
import threading

__autor__ = 'Hernani Aleman Ferraz'
__email__ = 'afhernani@gmail.com'
__apply__ = 'commun for autogif, guimovietogif'
__version__ = 1.0

class Movie:
    def __init__(self, file, remove=True):
        self.thread = None
        self.widget = None
        self.datos = {'time': 0, 'fps': 1, 'width': 1, 'height': 1, 'bitrate': 1, 'num': 1}
        self.exists = False
        self.file = " "
        self.path_file = " "
        self.datos['remove'] = remove
        if os.path.exists(file):
            self.exists = True
            self.file = os.path.split(file)[-1]
            self.path_file = os.path.dirname(file)
            self.datos['file'] = self.file
            self.datos['path_file'] = self.path_file
            self.datos['exists'] = self.exists
            self.datos['sucess'] = False

    def __str__(self, *args, **kwargs):
        return str(self.datos)

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
        print('extrac_informacion ->', self.datos['file'])
        if not self.datos['exists']:
            print('no se pudo extraer informacion del fichero')
            return
        movie = os.path.join(self.datos['path_file'], self.datos['file'])
        command = ['ffmpeg', '-i', movie]
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
                self.datos['time'] = total_sec
                print('hora, minuto, segundo:', t_hour, t_min, t_sec)
                print('total de segundos:', total_sec)

            # This matches1 is to get the frames por segundo
            matches1 = re.search(b'(?P<fps>(\d+.)* fps)', stdout)
            if matches1:
                print('fps ->', matches1['fps'])
                frame_rate = matches1['fps'].split(b' ')[0]
                self.datos['fps'] = float(frame_rate)
                print('fps ->', self.datos['fps'])

            matches2 = re.search(b' (?P<width>\d+)x(?P<height>\d{2,3}[, ])', stdout)
            if matches2:
                print(matches2)
                width = int(matches2['width'])
                height = int(matches2['height'].replace(b',', b' '))
                print('formato: ->', matches2, width, height)
                self.datos['width'] = width
                self.datos['height'] = height

            # averiaguar el ratio.
            matches3 = re.search(b'bitrate:\s{1}(?P<bitrate>\d+?)\s{1}', stdout)
            if matches3:
                print('matches3 ->', matches3['bitrate'])
                self.datos['bitrate'] = int(matches3['bitrate'])

        except subprocess.CalledProcessError as e:
            print(e.output)
            return
        self.datos['sucess'] = True
        print('extrac informacion from ->', self.datos['file'])
        print(self.datos)

    def extract_frames(self, file=None, num=None):
        '''
        extract frames from file
        param:
        file = file asignated, num = number of frames extract video to the gif
        return: Nathing, make num of image at directory thumbails maked
        '''
        print('extract frames from ->', self.datos['file'])
        if not self.datos['sucess']:
            print('no se pudo extraer informacion de', self.datos['file'])
            return
        if not self.datos['exists']:
            print('no se pudo extraer imagenes del fichero', self.datos['file'])
            return
        if not file:
            file = os.path.join(self.datos['path_file'], self.datos['file'])
        # obtener un nombre de fichero independiente del fichero y fichero de trabajo
        if not num:
            num = self.datos['num']
        import uuid
        name = str(uuid.uuid4()) + '-%04d.png'
        self.datos['code_frame'] = name
        # working file:
        working_file = os.path.join(self.datos['path_file'], 'Thumbails')
        self.datos['working_file'] = working_file
        if not os.path.exists(working_file):
            os.mkdir(working_file)
        # ficheros de frames de salida
        work_dir = os.path.join(working_file, name)
        # determinar los factores de la linea de comando.
        command = ['ffmpeg']
        valor = self.datos['time']
        if valor:
            valor = valor / (num + 1)
            if valor < 1: # no puede ser ziro
                valor = 1
        command.extend(['-ss', str(int(valor)), '-i', file, '-vf', 'fps=1/' + str(int(valor))
                           , '-vframes', str(num)
                           , work_dir, '-hide_banner'])
        print('Linea de comando ->', command)
        self.runCommand(command)
        print('end extract_frames from ->', self.datos['file'])
        print(self.datos)

    def make_gif_f_frames(self, framerate=1, scale='320:-1'):
        '''
        make a gif from cedec frames
        param:
            framerate=1, scale=Noen, xample: '200:-1' keep dimension format image
        return: Nothing, make file gif in ruth
        '''
        print('make gif from ->', self.datos['file'])
        if not self.datos['sucess']:
            print('no se pudo extraer informacion de', self.datos['file'])
            return
        if not self.datos['exists']:
            print('no se puedo crear el gif desde las imagenes de ->', self.datos['file'])
            return
        name = self.datos['code_frame']
        working_file = self.datos['working_file']
        work_dir = os.path.join(working_file, name)
        command = ['ffmpeg', '-y', '-framerate', str(framerate), '-i', work_dir] #, '-vf', 'scale=' + scale]
        
        if scale: # add scale if not nathing
            command2 = ['-vf', 'scale=' + scale]
            command.extend(command2)
        
        file_out = os.path.join(working_file, self.datos['file'] + '_thumbs_0000.gif')
        command.extend([file_out])
        print('create gif command ->', command)
        self.runCommand(command)
        # vamos a borrar los ficheros de imagen segun remove
        if self.datos['remove']:
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
        print('made gif  from ->', self.datos['file'])

    def make_gif(self):
        if self.datos['exists']:
            try:
                self.info_from_video()
                print('datos generales ->', self.datos)
                try:
                    self.extract_frames(num=16)
                    try:
                        self.make_gif_f_frames()
                    except Exception as e:
                        print('Exception make gif from frames', str(e.args))
                except Exception as e:
                    print('Exception extract_frames', str(e.args))
            except Exception as e:
                print('Exception info_from_video', str(e.args))
            print('datos generales ->', self.datos)
            if self.widget is not None:
                self.widget.event_generate('<<food>>', when='tail')

    def run(self):
        self.thread = threading.Thread(target=self.make_gif)
        self.thread.daemon = True
        self.thread.start()

    def isAlive(self):
        if self.thread is None:
            return False
        return self.thread.isAlive()

    def setwidget(self, widget=None):
        if widget is not None:
            self.widget = widget

