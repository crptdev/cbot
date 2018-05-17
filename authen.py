# -*- coding: utf-8 -*-
import os
import sqlite3
import sys
import hashlib
from log import Log

# ########### #
#  VARIABLE   #
# ########### #
__prog__    = 'authen'
__version__ = '0.001 Alpha'
__author__  = 'ELJIE'

class Authen():
	def __init__(self,DB_PATH, LogFile="database.log",PASSWORD_LENGTH_MIN=8, HASH_ALGORITHM='sha256'):
		self.PASSWORD_LENGTH_MIN = PASSWORD_LENGTH_MIN # Longueur minimum pour la création des utilisateur
		self.HASH_ALGORITHM = HASH_ALGORITHM # L'algorithme de hash à utiliser pour le stockage des mots de passe en base doit être : md5, sha1, sha224, sha256, sha384, sha512
		self.DB_PATH = DB_PATH
		self.LogFile = LogFile
		self.Logs = Log(self.LogFile)
		self.log = self.Logs.logger

	def db_exist(self):
		if os.path.exists(self.DB_PATH): 
			return True
			self.log.info( 'Base %s déjà existante' %self.DB_PATH )
		else:  
			self.log.info( 'Base %s n\'existe pas' %self.DB_PATH )
			return False

	def db_create(self):
		if self.db_exist():
			self.log.info(" Database déjà existante %s" % self.DB_PATH)
			return True
		db = self.db_connect()
		cursor = db.cursor()
		cursor.execute("CREATE TABLE users (username text PRIMARY KEY, password text);")
		self.log.info(" Database créée : %s" % self.DB_PATH)
		db.close()

	def db_connect(self):
		return sqlite3.connect(self.DB_PATH)


	def db_user_add(self,username,password):
		if len(password) < self.PASSWORD_LENGTH_MIN:
			self.log.error("Mot de passe doit etre supperieur à  %d characteres" % self.PASSWORD_LENGTH_MIN)
			return False
		else:
			hash_func = getattr(hashlib, self.HASH_ALGORITHM, None)
			if hash_func is None:
				self.log.error("Algo de Hash'%s' non trouvé" % self.HASH_ALGORITHM)
				return False
			password = hash_func(password.encode("UTF-8")).hexdigest()	
			db = self.db_connect()
			cursor = db.cursor()
			try:
				cursor.execute("INSERT INTO users VALUES (?, ?);", (username, password))
				self.log.info("L'utilisateur '%s' a été créé" % username)
			except sqlite3.IntegrityError:
				self.log.error("L'utilisateur '%s' existe déjà en base" % username)
				db.close()
				return False
			db.commit()
			db.close()
			return True

	def db_user_del(self,username):
		db = self.db_connect()
		cursor = db.cursor()
		cursor.execute("DELETE FROM users WHERE username = ?;", (username,))
		self.log.info("Suppression de l'utilisateur '%s'" % username)
		db.commit()
		db.close()
		return True

	def db_user_list(self):
		db = self.db_connect()
		cursor = db.cursor()
		cursor.execute("SELECT username FROM users;")
		users = cursor.fetchall()
		self.log.debug("Récuperation de la liste des utilisateurs")
		db.close()
		return users

	def db_user_authen(self,username,password):
		hash_func = getattr(hashlib, self.HASH_ALGORITHM)
		db = self.db_connect()
		cursor = db.cursor()
		cursor.execute('SELECT * FROM users WHERE username = ?;', (os.environ['username'],))
		result = cursor.fetchone()
		db.close()
		if result is None:
			return False
		username, password = result
		if hash_func(os.environ['password'].encode("utf-8")).hexdigest() != password:
			return False
		return True


if __name__ == "__main__":
	authen = Authen('./db_crypto.sqlite','activity.log')
	print( authen.db_exist() )
	authen.db_create()
	print( authen.db_exist() )
	print(authen.db_user_add('john Doe','password123456'))
	print(authen.db_user_add('Darth Vador','password123456'))
	print(authen.db_user_add('Louke Skyllehouheulkeurre','password123456'))
	print(authen.db_user_list() )
	print(authen.db_user_del('Louke Skyllehouheulkeurre') )
	print(authen.db_user_list() )
	print(authen.db_user_authen('Darth Vador','password') )
	print(authen.db_user_authen('Darth Vador','password123456') )
