#-*- coding:utf-8 -*-
import urllib
from urllib.request import urlopen
import json

# ########### #
#  VARIABLE   #
# ########### #
__prog__    = 'API'
__version__ = '0.001 Alpha'
__author__  = 'ELJIE'


Url = 'https://api.cryptowat.ch/markets/'

def f_get_trades(url):
    tab = []
    result = []
    try:
    	page = urlopen(url)
    except urllib.error.HTTPError:
    	return { "trades": [ { "error": "url 404" } ] }
    tab.append(  json.loads(page.read().decode("utf-8"))['result'] )
    for i in tab[0]:
            result.append(i)
    return result #tab


class Api():
	API_Authorized = [ 'trades', 'info', 'error']
	market_Authorized = ['kraken']
	def __init__(self, version):
		self.version(version)

	def version(self,numero=1):
		if numero == 1: self.version_api='public'
		if numero == 2: self.version_api='private'

	def get_api(self,**kwargs):
		action = kwargs.get('action')
		if action in self.API_Authorized:
			action = 'self.get_' + action +'(**kwargs)'
		else:
			action = 'self.get_error(**kwargs)'
		return eval(action)

	def get_error(self,**kwargs):
		from flask import abort
		abort(404)
		return "Get 404"


	def get_info(self,**kwargs):
		return "Get info"

	def get_trades(self,**kwargs):
		market = kwargs.get('market')
		pair   =  kwargs.get('pair')
		if market in self.market_Authorized:
			trades = f_get_trades(Url+ market + '/'+ pair +'/trades')
		else:
			trades = { "trades": [ { "error": "Milk 404" } ] }
		return trades





