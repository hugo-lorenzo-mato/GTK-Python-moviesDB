#!/usr/bin/python
#coding: utf-8 

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import sqlite3
from os.path import abspath, dirname, join, exists



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
		       Release         INT            NOT NULL,
		       Runtime		   INT,
		       Synopsis        TEXT,
		       Rating          INT);''')
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

	def insert_movie(self, tit, rel, run, syn, rat):
		# Insertamos la película en la base de datos
		sqlite_file = self.DB_DIR
		conn = sqlite3.connect(sqlite_file)
		c = conn.cursor()
		conn.execute("INSERT INTO MoviesDB (Id, Title,Release,Runtime,Synopsis,Rating) VALUES (?,?,?,?,?, ?)",\
					(None, tit, rel, run, syn, rat));
		conn.commit()
		conn.close()	

	def edit_movie(self, id_num, title,release,runtime,synopsis,rating):
		# Editamos la película en la base de datos
		sqlite_file = self.DB_DIR
		conn = sqlite3.connect(sqlite_file)
		c = conn.cursor()
		conn.execute("UPDATE MoviesDB SET Title = ?, Release = ?, Runtime = ?, Synopsis = ?, Rating = ?  WHERE Id = ?",\
		    		(title, release, runtime, synopsis, rating, id_num));
		conn.commit()
		conn.close()	 	

	def get_list_movies(self):
		lista = []
		sqlite_file = self.DB_DIR
		conn = sqlite3.connect(sqlite_file)
		cursor = conn.execute("SELECT Id, Title,Release,Runtime,Synopsis,Rating FROM MoviesDB") 
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
		cursor = conn.execute("SELECT Id, Title,Release,Runtime,Synopsis,Rating FROM MoviesDB") 
		for columna in cursor:
			if key in columna[1].lower() or key in columna[4].lower():
				lista.append(columna)
		conn.close()
		return lista			