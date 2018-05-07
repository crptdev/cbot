#-*- coding:utf-8 -*-
from flask import Flask, flash, redirect, render_template, request, session, abort
import json
import urllib
from urllib.request import urlopen
import os
import copy

# ########### #
#  VARIABLES  #
# ########### #
Market = 'bitfinex'
Pair = 'btcusd'
Url = 'https://api.cryptowat.ch/markets/'+ Market + '/'+ Pair +'/trades'
copie_result = []
# ##########
# FONCTION #
# ##########
def f_get_trades(url):
    tab = []
    result = []
    page = urlopen(url)
    tab.append(  json.loads(page.read().decode("utf-8"))['result'] )
    for i in tab[0]:
            result.append(i)
    return result #tab

def f_diff_tab(data,result):
  tab = []
  for a in result:
    if not(a in data):
      tab.append(a)
  if len(tab) == 0:
    tab.append(result[len(result)-1])
  return tab

def f_get_exchange_trades():
    trades = []
    trades = f_get_trades(Url)
    """
    print(Url)
    print(trades)
    """
    
    return trades
 
trades = f_get_exchange_trades()
print(trades)
print("=================================")
print(trades[0])
templates = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
print(templates)
#app = Flask(__name__, template_folder=templates)
app = Flask(__name__)

@app.route("/")
def index():
    global copie_result
    result = f_get_exchange_trades()
    copie_result = copy.deepcopy(result) 
    data = copy.deepcopy(copie_result) 
    result = f_diff_tab(data,result)
    return render_template('api.html',**locals())    
 
@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
