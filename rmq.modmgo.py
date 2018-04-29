import pika
import sys
import configparser 

import os
import urllib
import time
import json
import csv
import telegram

# fichier ini pour se connecter à la base Mongo du type :
#[mgo]
# Server=mango-36.atlantis.io:27017
# Base=clcw
# Coll=tradescol

#
def f_put_mgo(ot, chat_id, msg):
    msg =''
    for row in entetes:
            msg = msg + '<b>' + row + '</b>' + ','
    for row in data:
            msg = msg + str(row[1:len(row)])


    bot.send_message(chat_id=chat_id, text=msg, parse_mode=telegram.ParseMode.HTML)

def f_init_tlg(Tlgkey):
    bot = telegram.Bot(token=Tlgkey)
    return bot

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

def get_base(Server,Coll):
    from pymongo import MongoClient
    client = MongoClient(Server)
    db = client[Coll]
    return db

def main():
  
  Server, Base, Coll = f_Load_Conf(sys.argv[0][:-3]  + '.ini')
  print(Server + ' ' + Base + ' ' + Coll)
  db = get_base(Server,Coll)
   
  connection = pika.BlockingConnection(pika.ConnectionParameters(host=RMQServer))
  channel = connection.channel()
  channel.queue_declare(queue='mgo')
  
  def callback(ch, method, properties, body):
    # bot.send_message(chat_id=chat_id, text=str(body), parse_mode=telegram.ParseMode.HTML)
    print("Message Telegram" % body)
    print(body)
    

  channel.basic_consume(callback, queue='mgo', no_ack=True)

  print(' [*] Waiting for messages. To exit press CTRL+C')
  channel.start_consuming()
  
  

  
if __name__ == '__main__':
  main()
