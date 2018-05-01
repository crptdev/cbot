# Proposition : dans le cadre des agents et afin d'embarquer le monitoring, 
# utiliser le multithreading afin de traiter les actions metiers qui sont parfois en attente de messages (donc blocage dans une boucle)
# et en meme temps, envoyer des messages regulierement qui seront consommes dans mongo 
# et lu par une interface de monitoring capable d afficher l historique de l activite des agents distribues

import threading
import time
from random import randint

class ActionMetier(threading.Thread):
	def run(self):
		while True : 
			print('Nouveau Message! Action Metier')
			time.sleep(randint(0, 5))

class Monitoring(threading.Thread):
	def run(self):
		while True : 
			print('Send to queue : I am alive!')
			time.sleep(1)

if __name__ == '__main__':
	A = ActionMetier()
	A.start()
	B = Monitoring()
	B.start()
