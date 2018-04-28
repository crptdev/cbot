import pika
import sys
import configparser 

import os
import urllib
import time
import json
import csv
import telegram


RMQServer='seabunny.atlantis.io'

def f_put_tlg(bot, chat_id, msg):
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
	if conf.has_option('tlg', 'Tlgkey'):
		Tlgkey = conf.get ('tlg', 'Tlgkey')
		chat_id = conf.get ('tlg', 'chat_id')
	else:
		Tlgkey= ''
		chat_id= ''
	return Tlgkey, chat_id

def main():
  
  Tlgkey, chat_id = f_Load_Conf(sys.argv[0][:-3]  + '.ini')
  bot = f_init_tlg(Tlgkey)
   
  connection = pika.BlockingConnection(pika.ConnectionParameters(host=RMQServer))
  channel = connection.channel()
  channel.queue_declare(queue='tlg')
  
  def callback(ch, method, properties, body):
    bot.send_message(chat_id=chat_id, text=str(body), parse_mode=telegram.ParseMode.HTML)
    print("Message Telegram" % body)
    

  channel.basic_consume(callback, queue='tlg', no_ack=True)

  print(' [*] Waiting for messages. To exit press CTRL+C')
  channel.start_consuming()
  
  

  
if __name__ == '__main__':
  main()
