#!/usr/bin/python

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import Controlador_p1


Controlador_p1.Handler()
Gtk.main()