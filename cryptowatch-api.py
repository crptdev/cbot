# -*- coding:utf-8 -*-

# ####################
# Usage              #
# ####################
# Cryptowatch-api.py pourcentage secondes

# ####################
# API Non Officielle #
# ####################
# https://api.cryptowat.ch/markets/kraken/btcusd/events
# Indique les evenements survenus avec un timeStamp
# Ex : events

# https://api.cryptowat.ch/markets/summaries
# Recupere un resume sur toutes les places CryptoWatch
# Ex : summaries

# https://cryptowat.ch/auth/cat?view=market&exchange_slug=kraken&market_slug=kraken:btcusd
# ???


# ####################
#   API Officielle   #
# ####################
# https://cryptowat.ch/docs/api
# https://api.cryptowat.ch/assets                                                       Retourne toutes les monnaies traitées
# https://api.cryptowat.ch/assets/btc                                           Retourne tous les markets et les Pairs utilisée avec le BTC
# https://api.cryptowat.ch/pairingStatus()                                      Retourne toutes les pairs
# https://api.cryptowat.ch/pairs/ethbtc                                         Retourne la liste des marckets utilisant la Pair ethbtc
# https://api.cryptowat.ch/exchanges                                            Retourne la liste des Markets
# https://api.cryptowat.ch/exchanges/kraken                             Retourne les infos sur un seul market (Kraken)
# https://api.cryptowat.ch/markets                                                      Retourne la liste des pairs utilisées dans un market
# https://api.cryptowat.ch/markets/kraken                                       Retourne toutes les pairs d'un market
# https://api.cryptowat.ch/markets/gdax/btcusd                          Retourne les liens api vers Price; summary, orderbook, trades, ohlc
# https://api.cryptowat.ch/markets/gdax/btcusd/price            Retourne le prix
# https://api.cryptowat.ch/markets/gdax/btcusd/summary          Retourne Returns a market’s last price as well as other stats based on a 24-hour sliding window.
#                                                                                                                       ( High price - Low price - % change - Absolute change - Volume )
# https://api.cryptowat.ch/markets/gdax/btcusd/trades           Retourne par defaut les 50 dernier Trades [ ID, Timestamp, Price, Amount ]
# https://api.cryptowat.ch/markets/gdax/btcusd/orderbook        Retourne les ordres en cours [ Price, Amount ]
# https://api.cryptowat.ch/markets/kraken/btcusd/ohlc           Retourne les données du chandelier OHLC d'un marché [ CloseTime, OpenPrice, HighPrice, LowPrice, ClosePrice, Volume ]

# Nico : 0.002 Alpha : correctif delta, Args et Usage




try:
    # Pour Python 3.0 et +
    from urllib.request import urlopen
    python = 3
except ImportError:
    # Pour Python 2 --> urllib2
    from urllib2 import urlopen
    python = 2
import os
import urllib
import time
import json
import csv
import sys

# ##########
# VARIABLE #
# ##########
# __name__    = 'watchbot'
__version__ = '0.002 Alpha'
__author__  = 'ELJIE'

try :
        sys.argv[1], sys.argv[2]
except IndexError:
        print('\n USAGE : Cryptowatch-api.py pourcentage secondes\n')
        exit()

Pause = float(sys.argv[2])
Augment = float(sys.argv[1])

Url = 'https://api.cryptowat.ch/markets/bitfinex/btcusd/trades'
Achat = False
Banque = 100.
Qte = 0.
Fname  = 'Sortie.csv'
Entetes_csv = [ 'TimeStamp','Price','Volume']

# ##########
# FONCTION #
# ##########
def f_get_trades(url):
        tab = []
        result = []
        """
        if python == 3:
                with urllib.request.urlopen(url) as page: tab.append(  json.loads(page.read().decode())['result'] )
        else:
                page = urllib.urlopen(url)
                print(json.loads(page.read().decode()['result']  ) )
                tab.append(( json.loads(page.read()['result'] ) ))
        """
        page = urlopen(url)
        tab.append(  json.loads(page.read().decode("utf-8"))['result'] )
        for i in tab[0]:
                result.append(i)
        return result #tab

def f_put_csv(name='out.csv', data=[]):
        #file = open(name, "wb")
        #file = open(name, "w", newline="")
        if os.path.isfile(name):
                print("fichier ",name," existant")
                file = open(name, "a", newline="")
                writer = csv.writer(file)
        else:
                print("Nouveau Fichier de sortie", name)
                file = open(name, "w",  newline="")
                writer = csv.writer(file)
                writer.writerow( (Entetes_csv) )
        for row in data:
                writer.writerow( [ row[1], row[2], row[3] ] )

        file.close()




# ##########
#   MAIN   #
# ##########

def main():
        global Pause, Augment, Url, Achat, Banque, Qte
        data =[]
        start_time = time.time()
        data = f_get_trades(Url)
        dernier = []
        dernier.append(0)
        dernier.append((data[len(data)-1][1]))
        dernier.append((data[len(data)-1][2]))
        dernier.append((data[len(data)-1][3]))
        print("[ ] Pause de :",Pause, "s")

        while True : #pause:
                time.sleep(Pause)
                result =[]
                result = f_get_trades(Url)
                """
                result est de la forme :
                [ [ID, TimeStamp, Price, Volume] ,[ID, TimeStamp, Price, Volume], etc. ]
                """
                #print(result)
                f_put_csv(Fname, result)

                delta = result[len(result)-1][1] - dernier[1]
                print("[ ] Origin Price ",dernier[2], delta)

                if delta > Pause:
                        Last_Price = dernier[2]
                        New_Price = result[len(result)-1][2]
                        # Delta_Price = (result[len(result)-1][2] * 100/ Last_Price )- Last_Price
                        Delta_Price = New_Price / (Last_Price / 100 ) - 100

                        # """
                        print("TimeStamp Superieur à 1min => on calcul")
                        print("Last Price :",Last_Price)
                        print("New Price :", New_Price)
                        print("Delta Price :", New_Price - Last_Price, " Soit ", Delta_Price,"%")
                        # """

                        if Delta_Price >= Augment :
                                if Achat:
                                        if New_Price > SellPrice:
                                                print("[ ]")
                                                print("[+] Augmentation de " + str(Delta_Price)+"% => Ventre de " + str(Qte) + " a "+ str(New_Price))
                                                print("[+] == BENEFICE == " + str( (New_Price - SellPrice ) * Qte) )
                                                Achat = False
                                                SellPrice = 0.
                                                Banque += ( (New_Price - SellPrice ) * Qte)
                                                Qte =0





                                else:
                                        SellPrice = New_Price + 0
                                        Qte = Banque * 1.0 / LastPrice
                                        Banque -= Qte * LastPrice
                                        Achat = True
                                        print("[ ]")
                                        print("[+] Augmentation de " + str(Delta_Price)+"% => Achat de " + str(Qte) + " a "+ str(SellPrice))


                                print("[+] Banque : "+ str(Banque) + " - Qte : "+ str(Qte))



                        LastPrice = New_Price



        interval = time.time() - start_time
        print("Execution en seconds: ",interval)
        exit(0)

if __name__ == '__main__':
    main()

