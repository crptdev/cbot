#-*- coding:utf-8 -*-
import os

class WriteData():
  liste = []
  RMQServer = ''

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

    #return self.liste
    
  def get_rmq(self,**kwargs): 
  	flux = kwargs.get('flux')
  	msg = kwargs.get('msg')
    if name == None: return False
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.RMQServer))    

  def put_data(self,**kwargs): 
    for element in self.liste:
      e = 'self.put_data_' + element +'(**kwargs)'
      eval(e)

  def test(self,**kwargs):
    print(kwargs)
    print(kwargs.get('name') )
    print(kwargs.get('data') )
    print(kwargs.get('entetes') )
    
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
    name = kwargs.get('name')
    if name == None: return False
    data = kwargs.get('data') 
    if data == None: return False
    entetes = kwargs.get('entetes') 
    if entetes == None: return False
    if os.path.isfile(name):
      file = open(name, "a", newline="")
      writer = csv.writer(file)
    else:
      file = open(name, "w",  newline="")
      writer = csv.writer(file)
      writer.writerow( (entetes) )
    for row in data:
      #writer.writerow( (row[1:len(row)]) )
      writer.writerow( row )

    file.close()
    #print("je suis dans CSV\n================")
    

  def put_data_mongodb(self, name='out.csv', data=[], entetes=[]):
    1print("je suis dans MONGODB\n================")
    return False

if __name__ == '__main__':
  wd = WriteData('watchbot.tlg.ini')
  data = [['L1','L1','L1'], ['L2','L2','L2']]
  entetes =  [ 'Colonne 1','Colonne 2','Colonne 3']
  wd.put_data(name='sortie.csv',data=data,entetes=entetes)
  wd.test(media='toto', element=1)
