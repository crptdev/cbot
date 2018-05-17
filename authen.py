# -*- coding: utf-8 -*-
import os
import sqlite3
import sys
import hashlib


DB_PATH = './db_crypto.sqlite'
PASSWORD_LENGTH_MIN = 8 # Longueur minimum pour la création des utilisateur
# L'algorithme de hash à utiliser pour le stockage des mots de passe en base doit être :
# md5, sha1, sha224, sha256, sha384, sha512
HASH_ALGORITHM = 'sha256'

def db_exist(DB_PATH):
	if os.path.exists(DB_PATH): return True
	else:  return False

def db_create(DB_PATH):
	if db_exist(DB_PATH):
		#log("[-] : ERROR : Database déjà existante %s" % DB_PATH)
		return 
	db = db_connect(DB_PATH)
	cursor = db.cursor()
	cursor.execute("CREATE TABLE users (username text PRIMARY KEY, password text);")
	#log("[+] : Database créée : %s" % DB_PATH)


def db_connect(DB_PATH):
	if db_exist(DB_PATH):
		return sqlite3.connect(DB_PATH)
	else:
		return None

def db_user_add(DB_PATH,username,password):
	if len(password) < PASSWORD_LENGTH_MIN:
		#log("[-] : ERROR : Mot de passe doit etre supperieur à  %d characteres" % PASSWORD_LENGTH_MIN)
		return False
	else:
		hash_func = getattr(hashlib, HASH_ALGORITHM, None)
		if hash_func is None:
			#log("[-] : ERROR: Algo de Hash'%s' non trouvé" % HASH_ALGORITHM)
			return False
		password = hash_func(password.encode("UTF-8")).hexdigest()	
		db = db_connect(DB_PATH)
		cursor = db.cursor()
		try:
			cursor.execute("INSERT INTO users VALUES (?, ?);", (username, password))
		except sqlite3.IntegrityError:
			#log("[-] : ERROR : L'tilisteur '%s' existe déjà en base" % username)
			return False
		db.commit()
		return True

def db_user_del(DB_PATH,username):
	db = db_connect(DB_PATH)
	cursor = db.cursor()
	cursor.execute("DELETE FROM users WHERE username = ?;", (username,))
	db.commit()
	return True

def db_user_list(DB_PATH):
	db = db_connect(DB_PATH)
	cursor = db.cursor()
	cursor.execute("SELECT username FROM users;")
	users = cursor.fetchall()
	return users

def db_user_authen(DB_PATH,username,password):
	hash_func = getattr(hashlib, HASH_ALGORITHM)
	db = db_connect(DB_PATH)
	cursor.execute('SELECT * FROM users WHERE username = ?;', (os.environ['username'],))
	result = cursor.fetchone()
	if result is None:
		return False
	username, password = result
	if hash_func(os.environ['password'].encode("utf-8")).hexdigest() != password:
		return False
	return True


