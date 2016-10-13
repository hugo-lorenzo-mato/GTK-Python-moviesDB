#!/usr/bin/python
#coding: utf-8 

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import Controlador_p1


# Esto permite traducir los textos escritos

from os.path import abspath, dirname, join
import gettext
import locale

APP = 'MoviesDB'
DIR = abspath(dirname(__file__))
LOCALE_DIR = join(DIR, 'locale')

locale.setlocale(locale.LC_ALL, '')
locale.bindtextdomain(APP, LOCALE_DIR)
locale.textdomain(APP)

Controlador_p1.Handler()
Gtk.main()