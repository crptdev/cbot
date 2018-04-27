# -*- coding:utf-8 -*-

# ####################
# Usage              #
# ####################
# Cryptowatch-api.py pourcentage secondes
#
# Nico  : 0.002 Alpha : correctif delta, Args et Usage
# ELJIE : 0.002 Beta  : correctif delta, dernier, f_put_csv, variabilisation de Market et Pair Version Python >= 3.4
#


# Pour Python 3.0 et +
from urllib.request import urlopen

import os
import urllib
import time
import json
import csv
import sys

# ##########
# VARIABLE #
# ##########
__prog__    = 'watchbot'
__version__ = '0.003 Alpha'
__author__  = 'ELJIE'

Pause = 10
Augment = 5
Market = 'bitfinex'
Pair = 'btcusd'
Url = 'https://api.cryptowat.ch/markets/'+ Market + '/'+ Pair +'/trades'
Achat = False
Banque = 100.
Qte = 0.
Fname  = 'Sortie.csv'
Fachats_ventes = 'Achats-Ventes.csv'
Entetes_csv = [ 'TimeStamp','Price','Volume']
Entetes_Trades = [ 'TimeStamp','Pair','Transaction','Qte','Price','Bank']

Debug = False

if not Debug:
    try :
        sys.argv[1], sys.argv[2]
        Pause = float(sys.argv[2])
        Augment = float(sys.argv[1])

    except IndexError:
        print('\n USAGE : watchbot.py pourcentage secondes\n')
        exit(0)



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




# ##########
#   MAIN   #
# ##########

def main():
        global Pause, Augment, Url, Achat, Banque, Qte, Pair
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
                f_put_csv(Fname, result,Entetes_csv)

                delta = result[len(result)-1][1] - dernier[1]
                print("[ ] Origin Price ",dernier[2], delta)

                if delta > Pause:
                        Last_Price = dernier[2]
                        New_Price = result[len(result)-1][2]
                        # Delta_Price = (result[len(result)-1][2] * 100/ Last_Price )- Last_Price
                        Delta_Price = New_Price / (Last_Price / 100 ) - 100

                        if Debug:
                            print("TimeStamp Superieur à ", Pause, " => ", delta, " Tips")
                            print("Last Price :",Last_Price)
                            print("New Price :", New_Price)
                            print("Delta Price :", New_Price - Last_Price, " Soit ", Delta_Price,"%")
    
                        if Delta_Price >= Augment :
                                if Achat:
                                        if New_Price > SellPrice:
                                                print("[ ]")
                                                print("[+] Augmentation de " + str(Delta_Price)+"% => Vente de " + str(Qte) + " a "+ str(New_Price))
                                                print("[+] == BENEFICE == " + str( (New_Price - SellPrice ) * Qte) )
                                                Achat = False
                                                SellPrice = 0.
                                                Banque += ( (New_Price - SellPrice ) * Qte)
                                                Qte =0
                                                # Entetes_Trades = [ 'TimeStamp','Pair','Transaction','Qte','Price',Bank']
                                                #print(Fachats_ventes, [0,int(time.time()), 'Achat', Qte,New_Price,Banque],Entetes_Trades)
                                                f_put_csv(Fachats_ventes,[[0,int(time.time()),Pair,'Vente', Qte,New_Price,Banque]],Entetes_Trades)





                                else:
                                        SellPrice = New_Price + 0
                                        Qte = Banque * 1.0 / Last_Price
                                        Banque -= Qte * Last_Price
                                        Achat = True
                                        print("[ ]")
                                        print("[+] Augmentation de " + str(Delta_Price)+"% => Achat de " + str(Qte) + " a "+ str(SellPrice))
                                        f_put_csv(Fachats_ventes,[[0,int(time.time()),Pair,'Achat', Qte,SellPrice,Banque]],Entetes_Trades)


                                print("[+] Banque : "+ str(Banque) + " - Qte : "+ str(Qte))
                        dernier[1] = result[len(result)-1][1]
                        dernier[2] = result[len(result)-1][2]
                        dernier[3] = result[len(result)-1][3]
                        if Debug: print(dernier)



        interval = time.time() - start_time
        print("Execution en seconds: ",interval)
        exit(0)

if __name__ == '__main__':
    main()
