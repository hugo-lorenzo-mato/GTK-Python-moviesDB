#!/usr/bin/python
#coding: utf-8 

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class View(object):
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("uiP1.glade")
		main_window = self.builder.get_object("main_window")
		main_window.show()
		self.tree_view = self.builder.get_object("treeview_movies")
		self.liststore = self.builder.get_object("liststore_movies")
		self.scrolled_list = self.builder.get_object("scrolledwindow_movies")


	def confirm_movie(self, b, w):
		lista = []
		# Preparamos los contenedores
		title_entry = self.builder.get_object("entry_title")
		release_entry = self.builder.get_object("entry_release")
		runtime_entry = self.builder.get_object("entry_runtime")
		synopsis_entry = self.builder.get_object("entry_synopsis")
		rating_entry = self.builder.get_object("entry_rating")
		combo_entry = self.builder.get_object("comboboxtext_film_info")
		# Recuperamos el valor
		lista.append(title_entry.get_text())
		lista.append(int(release_entry.get_text()))
		lista.append(int(runtime_entry.get_text()))
		lista.append(synopsis_entry.get_text())
		lista.append(int(rating_entry.get_text()))
		lista.append(combo_entry.get_active())
		# Nos servimos de tree iterator para recuperar los datos de la fila seleccionada
		select = self.tree_view.get_selection()
		model, treeiter = select.get_selected()
		try:
			id_num = self.liststore[treeiter][0]
			lista.append(id_num)
			# Limpiamos las entradas de los datos anteriores
			title_entry.set_text("")
			runtime_entry.set_text("")
			release_entry.set_text("")
			synopsis_entry.set_text("")
			rating_entry.set_text("")
			return lista

		except:
			lista.append(None)
			# Limpiamos las entradas de los datos anteriores
			title_entry.set_text("")
			runtime_entry.set_text("")
			release_entry.set_text("")
			synopsis_entry.set_text("")
			rating_entry.set_text("")
			return lista
		

	def cancel_add(self, b, w):
		title_entry = self.builder.get_object("entry_title")
		release_entry = self.builder.get_object("entry_release")
		runtime_entry = self.builder.get_object("entry_runtime")
		synopsis_entry = self.builder.get_object("entry_synopsis")
		rating_entry = self.builder.get_object("entry_rating")
		combo_entry = self.builder.get_object("comboboxtext_film_info")
		# Limpiamos las entradas de los datos anteriores
		title_entry.set_text("")
		runtime_entry.set_text("")
		release_entry.set_text("")
		synopsis_entry.set_text("")
		rating_entry.set_text("")
		combo_entry.set_active(0)

	def edit_film(self, b, w):
		# Nos servimos de tree iterator para recuperar los datos de la fila seleccionada
		select = self.tree_view.get_selection()
		model, treeiter = select.get_selected()
		title = self.liststore[treeiter][1]
		release = int(self.liststore[treeiter][2])
		runtime = int(self.liststore[treeiter][3])
		synopsis = self.liststore[treeiter][4]
		rating = int(self.liststore[treeiter][5])
		watched = int(self.liststore[treeiter][6])
		# Preparamos los contenedores
		title_entry = self.builder.get_object("entry_title")
		release_entry = self.builder.get_object("entry_release")
		runtime_entry = self.builder.get_object("entry_runtime")
		synopsis_entry = self.builder.get_object("entry_synopsis")
		rating_entry = self.builder.get_object("entry_rating")
		combo_entry = self.builder.get_object("comboboxtext_film_info")
		title_entry.set_text(title)
		release_entry.set_text(str(release))
		runtime_entry.set_text(str(runtime))
		synopsis_entry.set_text(synopsis)
		rating_entry.set_text(str(rating))
		if watched == 1:
			combo_entry.set_active(1)
		else:
			combo_entry.set_active(0)



	def delete_film(self, b, w):		
		select = self.tree_view.get_selection()
		model, treeiter = select.get_selected()
		id_num = self.liststore[treeiter][0]
		model.remove(treeiter)
		return id_num

	def search_clicked(self, b, w):
		search_entry = self.builder.get_object("searchentry")
		key = search_entry.get_text()
		search_entry.set_text("")
		return key.lower()

	def show_list(self, lista):
		self.liststore.clear()
		for i in range(len(lista)):
			self.liststore.append([lista[i][0], lista[i][1], lista[i][2], lista[i][3], lista[i][4], lista[i][5], lista[i][6] ])

	def show_list_restoreCombo(self, lista):
		self.liststore.clear()
		for i in range(len(lista)):
			self.liststore.append([lista[i][0], lista[i][1], lista[i][2], lista[i][3], lista[i][4], lista[i][5], lista[i][6] ])
		combo_info = self.builder.get_object("comboboxtext")
		combo_info.set_active(0)

	def check_combobox(self, b):
		combo_info = self.builder.get_object("comboboxtext")
		return combo_info.get_active()
		
	def recommended_clicked(self, b):
		select = self.tree_view.get_selection()
		model, treeiter = select.get_selected()
		title = self.liststore[treeiter][1]
		return title	
