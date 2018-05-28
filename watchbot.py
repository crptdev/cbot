# -*- coding:utf-8 -*-

# ####################
# Usage              #
# ####################
# 
#
# Nico  : 0.002 Alpha : correctif delta, Args et Usage
# ELJIE : 0.002 Beta  : correctif delta, dernier, f_put_csv, variabilisation de Market et Pair Version Python >= 3.4
# Nico  : 0.002 Gamma : Ajout telegramme
# ELJIE : 0.003 Alpha : 
# ELJIE : 0.004 Alpha : Ajout de Alive + Thread


# Pour Python 3.0 et +
from urllib.request import urlopen

import os
import urllib
import time
import json
import csv
import sys
from tlg import TelegramBOT #telegram
from writedata import WriteData
from threading import Thread

import configparser

import copy




# ##########
# VARIABLE #
# ##########
__prog__    = 'watchbot'
__version__ = '0.004 Alpha'
__author__  = 'ELJIE'

Pause = 10
Augment = 1 #5
Market = 'bitfinex'
Pair = 'btcusd'
Url = 'https://api.cryptowat.ch/markets/'+ Market + '/'+ Pair +'/trades'
Achat = False
Banque = 100.
Qte = 0.
Fname  = 'Sortie.csv'
Fachats_ventes = 'Achats-Ventes.csv'
Entetes_csv = [ 'TimeStamp','Price','Volume']
Entetes_Trades = [ 'TimeStamp','Market','Pair','Transaction','Qte','Price','Bank']
Tlgkey='tokenbot' 
Host = 'MicroService1'


Debug = True

if not Debug:
    try :
        sys.argv[1], sys.argv[2]
        Pause = float(sys.argv[2])
        Augment = float(sys.argv[1])

    except IndexError:
        print('\n USAGE : watch.py pourcentage secondes\n')
        exit(0)


# #################
# Class Temporaire
# #################
class ALive(Thread):
    """Thread chargé simplement d'indiquer sa vie."""
    def __init__(self,**kwargs): #wd, host,attente=5,debug=False):
        Thread.__init__(self)
        self.bool = True
        self.wd = kwargs.get('wd')        
        self.host = kwargs.get('host')
        self.attente = kwargs.get('attente')
        self.debug = kwargs.get('debug')
        if self.attente == None : self.attente = 5
        if self.debug == None : self.debug = False


    def run(self):
        """Code à exécuter pendant l'exécution du thread."""

        i = 0
        while self.bool :
            if i == 0: 
                etat = 'start'
                i += 1
            else: 
                etat = 'alive'
            message =  [  self.host, etat] 
            #self.wd.put_data(collection='alive',pair=int(time.time()),data= message )
            self.wd.put_data( base='alive', collection='etat',pair=str(int(time.time())),data= [ self.host, etat ] )
            if self.debug:
                sys.stdout.write(str(message)+ str(self.bool))
                sys.stdout.flush()
            time.sleep(self.attente)

    def stop(self):
        self.bool = False
        self.wd.put_data(base ='alive', collection='etat',pair=str(int(time.time())),data= [ self.host, 'stop' ] )
        if self.debug: print("-- Fin --")

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
    return result 

def f_put_csv(name='out.csv', data=[], entetes=[]):
    if os.path.isfile(name):
            if Debug: print("[D] fichier ",name," existant")
            file = open(name, "a", newline="")
            writer = csv.writer(file)
    else:
            if Debug: print("[D] Nouveau Fichier de sortie", name)
            file = open(name, "w",  newline="")
            writer = csv.writer(file)
            writer.writerow( (entetes) )
    for row in data:
            writer.writerow( (row[1:len(row)]) )
    file.close()

def f_put_tlg(bot, chat_id,data=[], entetes=[]):
    msg =''
    for row in entetes:
            msg = msg + '<b>' + row + '</b>' + ','
    for row in data:
            msg = msg + str(row[1:len(row)])

    bot.sendMessage(chat_id, msg)
    print("---------------------")
    print(msg)
    print("---------------------")
    


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

def f_diff_tab(data,result):
  tab = []
  for a in result:
    if not(a in data):
      tab.append(a)
  if len(tab) == 0:
    tab.append(result[len(result)-1])
  return tab

def f_put_data(result):
  
  pass

# ##########
#   MAIN   #
# ##########

def main(): 
    global Pause, Augment, Url, Achat, Banque, Qte, Pair, Market, Host
    Tlgkey, chat_id = f_Load_Conf(sys.argv[0][:-3]  + '.ini')
    bot=TelegramBOT(Tlgkey, chat_id)
    wd = WriteData(sys.argv[0][:-3] + '.ini') 
    # Création du thread ALive
    thread_1 = ALive(wd=wd,host=Host,debug=True)
    # Lancement du thread ALive
    thread_1.start()

    data =[]
    start_time = time.time()
    data = f_get_trades(Url)
    dernier = []
    dernier.append(0)
    dernier.append((data[len(data)-1][1]))
    dernier.append((data[len(data)-1][2]))
    dernier.append((data[len(data)-1][3]))
    print("[ ] Pause de :",Pause, "s")

    while True : 
            time.sleep(Pause)
            result =[]
            result = f_get_trades(Url)
            copie_result = copy.deepcopy(result)
            """
            result est de la forme :
            [ [ID, TimeStamp, Price, Volume] ,[ID, TimeStamp, Price, Volume], etc. ]
            """
            #print(result)

            # Injection des tableaux dans MongoDB
            ## Delta entre data et result
            result = f_diff_tab(data,result)
            ## Injection dans csv et mongo
            wd.put_data(name=Fname,data=result,entetes=Entetes_csv)         
            
            delta = result[len(result)-1][1] - dernier[1]
            print("[ ] Origin Price ",dernier[2], delta)
            if delta > Pause:
                    Last_Price = dernier[2]
                    New_Price = result[len(result)-1][2]
                    # Delta_Price = (result[len(result)-1][2] * 100/ Last_Price )- Last_Price
                    Delta_Price = New_Price / (Last_Price / 100 ) - 100
                    if False: #Debug:
                        print("TimeStamp Superieur à ", Pause, " => ", delta, " Tips")
                        print("Last Price :",Last_Price)
                        print("New Price :", New_Price)
                        print("Delta Price :", New_Price - Last_Price, " Soit ", Delta_Price,"%")
                    if Delta_Price >= Augment :
                            if Achat:
                                    if New_Price > 0: #SellPrice:
                                            print("[ ]")
                                            print("[+] Augmentation de " + str(Delta_Price)+"% => Vente de " + str(Qte) + " a "+ str(New_Price))
                                            print("[+] == BENEFICE == " + str( (New_Price - SellPrice ) * Qte) )
                                            Achat = False
                                            SellPrice = 0.
                                            Banque += ( (New_Price - SellPrice ) * Qte)
                                            Qte =0
                                            # Entetes_Trades = [ 'TimeStamp','Pair','Transaction','Qte','Price',Bank']
                                            #print(Fachats_ventes, [0,int(time.time()), 'Achat', Qte,New_Price,Banque],Entetes_Trades)
                                            #f_put_csv(Fachats_ventes,[[0,int(time.time()),Market,Pair,'Vente', Qte,New_Price,Banque]],Entetes_Trades)
                                            wd.put_data(base='kraken',collection='btcusd',pair='btcusd',name=Fachats_ventes,data=[[0,int(time.time()),Market,Pair,'Vente', Qte,New_Price,Banque]],entetes=Entetes_Trades)  
                                            f_put_tlg(bot,chat_id,[[0,int(time.time()),Market,Pair,'Vente', Qte,New_Price,Banque]],Entetes_Trades)

                            else:
                                    SellPrice = New_Price + 0
                                    Qte = Banque * 1.0 / Last_Price
                                    Banque -= Qte * Last_Price
                                    Achat = True
                                    print("[ ]")
                                    print("[+] Augmentation de " + str(Delta_Price)+"% => Achat de " + str(Qte) + " a "+ str(SellPrice))
                                    #f_put_csv(Fachats_ventes,[[0,int(time.time()),Market,Pair,'Achat', Qte,SellPrice,Banque]],Entetes_Trades)
                                    wd.put_data(base='kraken',collection='btcusd',pair='btcusd',name=Fachats_ventes,data=[[0,int(time.time()),Market,Pair,'Achat', Qte,SellPrice,Banque]],entetes=Entetes_Trades)  
                                    f_put_tlg(bot,chat_id,[[0,int(time.time()),Market,Pair,'Achat', Qte,SellPrice,Banque]],Entetes_Trades)

                            print("[+] Banque : "+ str(Banque) + " - Qte : "+ str(Qte))
                    dernier[1] = result[len(result)-1][1]
                    dernier[2] = result[len(result)-1][2]
                    dernier[3] = result[len(result)-1][3]
                    if Debug: print(dernier)
            data = copy.deepcopy(copie_result)


    interval = time.time() - start_time
    print("Execution en seconds: ",interval)
    exit(0)

if __name__ == '__main__':
    main()
