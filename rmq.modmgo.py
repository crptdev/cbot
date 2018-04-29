import pika
import sys
import configparser 

import os
import urllib
import time
import json
import csv
import telegram
import pandas as pd

RMQServer='seabunny.atlantis.io'

# fichier ini pour se connecter a la base Mongo du type :
# [mgo]
# Server=mango-36.atlantis.io:27017
# Base=clcw
# Coll=tradescol

#

def f_Load_Conf(Fic):
	conf =configparser.ConfigParser ()
	conf .readfp (open (Fic))
	#logger.info('Lecture du fichier %s', Fic)
	if conf.has_option('mgo', 'Base'):
		Server = conf.get ('mgo', 'Server')
		Base = conf.get ('mgo', 'Base')
		Coll = conf.get ('mgo', 'Coll')
	else:
		Server = ''
		Base = ''
		Coll = ''
	return Server,Base,Coll

def get_base(Server,Base):
    from pymongo import MongoClient
    client = MongoClient(Server)
    db=client.clcw
    return db

def main():
  
  Server, Base, Coll = f_Load_Conf(sys.argv[0][:-3]  + '.ini')
  print(Server + ' ' + Base + ' ' + Coll)
  base = get_base(Server,Base)
   
  connection = pika.BlockingConnection(pika.ConnectionParameters(host=RMQServer))
  channel = connection.channel()
  channel.queue_declare(queue='mgo')
  
  def callback(ch, method, properties, body):
    print("Message Telegram" % body)
    data = json.loads(body.decode("utf-8"))
    base.trades.insert_many(data)

  channel.basic_consume(callback, queue='mgo', no_ack=True)

  print(' [*] Waiting for messages. To exit press CTRL+C')
  channel.start_consuming()
  
  

  
if __name__ == '__main__':
  main()
