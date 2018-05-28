#-*- coding:utf-8 -*-
import os

__version__ = '0.001 28/05/2018'

class WriteData():
  liste = []
  RMQServer = ''
  action = []

  def __init__(self, fic):
    self.load_conf(fic)

    
  def load_conf(self,fic):
    import configparser
    conf =configparser.ConfigParser ()
    conf.readfp(open(fic) )
    for parametre, valeur in conf['DataWrite'].items():
        if eval(valeur): self.liste.append(parametre)
        if parametre == 'rmq': 
          self.RMQServer = conf.get(parametre, 'RMQServer')
        if parametre == 'mongodb':
          self.server = conf.get(parametre, 'Server')
          self.base = conf.get(parametre, 'Base')
        if parametre == 'csv':
          self.name = conf.get(parametre, 'Name')
    self.action = ['rmq', 'csv', 'mongodb']

 
  def get_rmq(self,**kwargs): 
    import pika
    if flux == None: return False
    flux = kwargs.get('flux')
    msg = kwargs.get('msg')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.RMQServer))    

  def put_data(self,**kwargs): 
    for element in self.liste:
      if element in self.action:
        e = 'self.put_data_' + element +'(**kwargs)'
        eval(e)
      else:
        print("[KO] - parametre '{}'' non reconnu".format(element) )

  def put_data_rmq(self, **kwargs): #name='out.csv', data=[], entetes=[]):
    import pika
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.RMQServer))
    channel = connection.channel()
    channel.queue_declare(queue='tlg')
    channel.basic_publish(exchange='', routing_key='tlg', body=msg)
    print(" [x] Sent " + msg )
    connection.close()
    return False

  def put_data_csv(self, **kwargs): #name='out.csv', data=[], entetes=[]):
    import csv
    name = self.name
    data = kwargs.get('data') 
    entetes = kwargs.get('entetes') 
    if name == None: return False
    if data == None: return False
    if entetes == None: return False
    if os.path.isfile(name):
      file = open(name, "a", newline="")
      writer = csv.writer(file)
    else:
      file = open(name, "w",  newline="")
      writer = csv.writer(file)
      writer.writerow( (entetes) )
    for row in data:
      writer.writerow( row )

    file.close()

    

  def put_data_mongodb(self, **kwargs): 
    data = kwargs.get('data') 
    pair = kwargs.get('pair')     
    if not(kwargs.get('base') == None): self.base = kwargs.get('base')
    if kwargs.get('collection') == None: collection = 'ATraiter'
    else: collection = kwargs.get('collection')
    if data == None: return False
    if pair == None: return False
    print(kwargs)

    from pymongo import MongoClient, errors
    import datetime
    try:
      client = MongoClient('mongodb://'+self.server+'/')
      db = client[self.base]
      table = db[collection] 
      post = self._convert_tab_to_json(collection,pair,data)
      post_id = table.insert(post)
      print("[OK] - Connexion réussie sur MongoDB : {} à la collection {} de la base : {}".format(self.server,collection,self.base))

    except errors.ConnectionFailure as e:
      print( "[KO] - Erreur sur Connexion à MongoDB : %s" % e)

  def _convert_tab_to_json(self,market,pair,data):
    json = { } 
    donnee={}
    donnee[pair] = data 
    json.update(donnee)
    return json



  def test(self,**kwargs):
    print(kwargs)
    print(kwargs.get('name') )
    print(kwargs.get('data') )
    print(kwargs.get('entetes') )

if __name__ == '__main__':
  wd = WriteData('watchbot.tlg.ini')
  def f_get_trades(url):
    from urllib.request import urlopen
    import json
    tab = []
    result = []
    page = urlopen(url)
    tab.append(  json.loads(page.read().decode("utf-8"))['result'] )
    for i in tab[0]:
            result.append(i)
    return result 
  data = f_get_trades('https://api.cryptowat.ch/markets/bitfinex/btcusd/trades')
  #data = [['L1','L1','L1'], ['L2','L2','L2']]
  print(data)
  entetes =  [ 'Colonne 1','Colonne 2','Colonne 3']
  wd.put_data(base='kraken',collection='btcusd',pair='btcusd',data=data,entetes=entetes)
  wd.test(media='toto', element=1)
