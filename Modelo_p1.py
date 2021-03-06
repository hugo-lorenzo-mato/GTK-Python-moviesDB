#!/usr/bin/python
#coding: utf-8 

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import sqlite3
from os.path import abspath, dirname, join, exists

import tmdbsimple as tmdb
tmdb.API_KEY = '1c10532950c7f32f612ee2a3c403a56a'
import requests


class Model(object):
	
	def __init__(self):
		self.DIR = abspath(dirname(__file__))
		# Cremamos una base de datos en la dirección desde la que se ejecuta el programa
		self.DB_DIR = join(self.DIR, "Movies_DB.sqlite")

	def connection(self):
		# Data base creation and connection 
		sqlite_file = self.DB_DIR
		if exists(sqlite_file):
			print("DB Exists!")
		else:
			conn = sqlite3.connect(sqlite_file)
			c = conn.cursor()
			print("It doesn't exist! \nCreating ....")
			# No hace falta insertar autoincrement dado que ya se lo aplica
			conn.execute('''CREATE TABLE MoviesDB
			  (Id   INTEGER    PRIMARY KEY, 
		       Title 		   TEXT           NOT NULL,
		       Release         INT,
		       Runtime		   INT,
		       Synopsis        TEXT,
		       Rating          INT,
		       Watched		   INT);''')
			conn.commit()
			conn.close()
			print ("Table created successfully");


	def remove_film(self, id_Num):
		# Preparamos la conexion y extraemos de la BD los datos
		sqlite_file = self.DB_DIR
		conn = sqlite3.connect(sqlite_file)
		cursor=conn.cursor()
		cursor.execute("DELETE FROM MoviesDB where Id = ?;", (id_Num, ))
		conn.commit()
		conn.close()		

	def insert_movie(self, tit, rel, run, syn, rat, wat):
		# Insertamos la película en la base de datos
		sqlite_file = self.DB_DIR
		conn = sqlite3.connect(sqlite_file)
		c = conn.cursor()
		conn.execute("INSERT INTO MoviesDB (Id, Title,Release,Runtime,Synopsis,Rating, Watched) VALUES (?,?,?,?,?,?,?)",\
					(None, tit, rel, run, syn, rat, wat));
		conn.commit()
		conn.close()	

	def edit_movie(self, id_num, title,release,runtime,synopsis,rating, watched):
		# Editamos la película en la base de datos
		sqlite_file = self.DB_DIR
		conn = sqlite3.connect(sqlite_file)
		c = conn.cursor()
		conn.execute("UPDATE MoviesDB SET Title = ?, Release = ?, Runtime = ?, Synopsis = ?, Rating = ?, Watched = ?  WHERE Id = ?",\
		    		(title, release, runtime, synopsis, rating, watched, id_num));
		conn.commit()
		conn.close()	 	

	def get_list_movies(self):
		lista = []
		sqlite_file = self.DB_DIR
		conn = sqlite3.connect(sqlite_file)
		cursor = conn.execute("SELECT Id, Title,Release,Runtime,Synopsis,Rating, Watched FROM MoviesDB") 
		lista.clear()
		for columna in cursor:
			lista.append(columna)
		conn.close()
		return lista

	def check_exists(self, id_num):
		sqlite_file = self.DB_DIR
		conn = sqlite3.connect(sqlite_file)
		cursor = conn.execute("SELECT Title FROM MoviesDB WHERE Id = ?", (id_num, )) 
		data=cursor.fetchone()
		if data is None:
			return False
		else:
			return True
		conn.close()

	def search(self, key):
		lista = []
		sqlite_file = self.DB_DIR
		conn = sqlite3.connect(sqlite_file)
		cursor = conn.execute("SELECT Id, Title,Release,Runtime,Synopsis,Rating, Watched FROM MoviesDB") 
		for columna in cursor:
			if key in columna[1].lower() or key in columna[4].lower():
				lista.append(columna)
		conn.close()
		return lista			

	def search_by(self, combo_id):
		combo_list = []
		sqlite_file = self.DB_DIR
		conn = sqlite3.connect(sqlite_file)
		cursor = conn.execute("SELECT Id, Title,Release,Runtime,Synopsis,Rating, Watched FROM MoviesDB") 		
		if combo_id == 1:
			for columna in cursor:
				if columna[6] == 1:
					combo_list.append(columna)
			conn.close()
			return combo_list
		elif combo_id == 2:
			for columna in cursor:
				if columna[6] == 0:
					combo_list.append(columna)
			conn.close()
			return combo_list
		else:
			return None
			
	def check_exists_title(self, title):
		sqlite_file = self.DB_DIR
		conn = sqlite3.connect(sqlite_file)
		cursor = conn.execute("SELECT Title FROM MoviesDB WHERE Title = ?", (title, )) 
		data=cursor.fetchone()
		if data is None:
			return False
		else:
			return True
		conn.close()
			
			
	def recommended(self, title):
		lista = []
		# Primero se busca la película por título (ya que no contamos con
		# ids de tmdb propias)
		search = tmdb.Search()
		response = search.movie(query= title)
		if search.results == []:
			return lista
		s = search.results[0]
		num = int(s['id'])
		mov = tmdb.Movies(num)
		# Se obtiene un diccionario de las películas similares
		response = mov.similar_movies()
		results = response['results']
		i = 0
		# Bucle limitado a 5 vueltas o menos para reducir volumen
		for s in results:
			num = int(s['id'])
			mov = tmdb.Movies(num)
			mov.info()
			# Se obtiene información de los campos pertinentes
			title = mov.title
			release = mov.release_date
			release = int(release[0:4]) 	# Sólo necesitamos el año
			runtime = int(mov.runtime)
			synopsis = mov.overview
			rating = int((mov.vote_average)/2)
			# Se comprueba que no se inserten películas ya existentes
			if not self.check_exists_title(title):
				self.insert_movie(title, release, runtime, synopsis, \
				rating, 0)
				i = i+1
				if i == 5:
					break
