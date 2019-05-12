#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os

__autor__ = 'Hernani Aleman Ferraz'
__email__ = 'afhernani@gmail.com'
__apply__ = 'by autogif'
__version__ = 1.0

def items_only_a(path=None):
    '''
    compara directorios raiz e hijo Thumbails
    y encuentra los no thumbailsables del raiz.
    and gets the thumbails not relationship with path
    path= dir of work
    Return: list files not in down, list files not in out
    '''
    if not path:
        print('path not deffined')
        return
    dirwork = os.path.abspath(path)
    if not os.path.isdir(dirwork):
        print('path not is a directory', dirwork)
        return
    listbase = os.listdir(dirwork)
    # print('listbase ->', listbase)
    listbasemod = []
    for item in listbase:
        filefound = os.path.join(dirwork, item)
        if os.path.isdir(os.path.abspath(filefound)):
            print('es un directorio')
            continue
        listbasemod.append(item + '_thumbs_0000.gif')
    # print('listabasemod ->', listbasemod)
    listextend = os.listdir(path + '/Thumbails')
    # print('listextend ->', listextend)
    a = set(listbasemod)-set(listextend)
    # elementos que solo estan en a
    b = list(a)
    c = []
    for item in b:
        c.append(item.split('_thumbs_0000.gif')[0])
    # elementos solo en b
    d = set(listextend) - set(listbasemod)
    f = list(d)
    # print('elementos solo en b -->', f)
    return c, f


if __name__ == '__main__':
    print('items_only_a ---------------------------------')
    print(items_only_a('work/videos'))
