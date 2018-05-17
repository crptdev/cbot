# -*- coding: utf-8 -*-
import logging
from logging.handlers import RotatingFileHandler

# ########### #
#  VARIABLE   #
# ########### #
__prog__    = 'log'
__version__ = '0.001 Alpha'
__author__  = 'ELJIE'

class Log():
	def __init__(self,log_file) :
		self.logFile = log_file
		self.logger = logging.getLogger()
		self.logger.setLevel(logging.DEBUG)
		self.formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
		self.file_handler = RotatingFileHandler(self.logFile, 'a', 1000000, 1)
		self.file_handler.setLevel(logging.DEBUG)
		self.file_handler.setFormatter(self.formatter)
		self.logger.addHandler(self.file_handler)
		self.stream_handler = logging.StreamHandler()
		self.stream_handler.setLevel(logging.DEBUG)
		self.logger.addHandler(self.stream_handler)
