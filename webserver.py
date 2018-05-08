#-*- coding:utf-8 -*-
from flask import Flask, flash, redirect, render_template, session, abort
from flask import request # permet de recuperer la requette HTTP Cliente
from flask import make_response # permet de modofier le mimetype lors d'une réponse
from flask import jsonify # permet de JSONifier une reponse HTML
import json
import urllib
from urllib.request import urlopen
import os
import copy
from api import Api

# ########### #
#  VARIABLE   #
# ########### #
__prog__    = 'webserver'
__version__ = '0.001 Alpha'
__author__  = 'ELJIE'

Debug = True



app = Flask(__name__)
app.debug = Debug
app.secret_key = '2d9-E2.)f&é,A$p@fpa+zSU03êû9_'

@app.route("/")
def hello():
	affichage = "Hello World! <BR>"
	return affichage


@app.route('/api/v1/')
@app.route('/api/v1/<string:action>', methods=['GET'])
@app.route('/api/v1/<string:action>/<market>/<pair>', methods=['GET'])
def api_v1(**kwargs):
	ret = api_V1.get_api(**kwargs)
	return jsonify(ret)

if __name__ == "__main__":
    api_V1 = Api(1)    
    app.run()
