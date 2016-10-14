#!/usr/bin/python
#coding: utf-8 

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import Modelo_p1
import Vista_p1


class Handler(object):

	def __init__(self):
		self.modelo = Modelo_p1.Model()
		self.conecction = self.modelo.connection()
		self.vista = Vista_p1.View()
		self.vista.builder.connect_signals(self)
		self.lista = self.modelo.get_list_movies()
		self.vista.show_list(self.lista)

	def on_delete_window(self, w):
		Gtk.main_quit()
		
	def on_button_confirm_movie(self, b):
		self.lista = self.vista.confirm_movie(self, b)
		if self.lista[6] != None:
			self.modelo.edit_movie(self.lista[6], self.lista[0],  \
								   self.lista[1], self.lista[2],  \
								   self.lista[3], self.lista[4], self.lista[5])  
		else:
			self.modelo.insert_movie(self.lista[0], self.lista[1],  \
								     self.lista[2], self.lista[3],  \
								     self.lista[4], self.lista[5])  
		self.lista = self.modelo.get_list_movies()
		self.vista.show_list_restoreCombo(self.lista)			


	def on_Button_Edit(self, b, b2, w):
		self.vista.edit_film(self, b)


	def on_button_cancel_movie(self, b):
		self.vista.cancel_add(self, b)
		self.lista = self.modelo.get_list_movies()
		# Volvemos a mostrar la lista y nos desmarca anteriores pulsaciones en la lista
		self.vista.show_list(self.lista)

	def on_Button_Delete(self, b):
		id_num = self.vista.delete_film(self, b)
		Modelo_p1.Model().remove_film(id_num)

	def on_button_search_clicked(self, b):
		key = self.vista.search_clicked(self, b)
		self.lista = self.modelo.search(key)
		self.vista.show_list(self.lista)

	def on_reload_list(self, b):
		self.lista = self.modelo.get_list_movies()
		self.vista.show_list(self.lista)

	def on_comboboxtext_changed(self,b):
		combo_id = self.vista.check_combobox(b)
		if combo_id == 0:
			self.lista = self.modelo.get_list_movies()
			self.vista.show_list(self.lista)
		else:	
			self.lista = self.modelo.search_by(combo_id)
			self.vista.show_list(self.lista)

	def on_button_recommended(self, b):
		# Se obtiene el título de la película de la vista
		title = self.vista.recommended_clicked(b)
		self.modelo.recommended(title)
		self.lista = self.modelo.get_list_movies()
		self.vista.show_list_restoreCombo(self.lista)
