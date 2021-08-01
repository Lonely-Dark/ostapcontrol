#!/usr/bin/env python
# -*- coding: utf8 -*-

# ---Lonely_Dark---
# Python 3.9.6

import requests
import logging
from Requests import Requests

# Create registrator with name engine
module = logging.getLogger('main.engine')

class Engine(Requests):

	def __init__(self):
		# Create registrator with name engine.Engine
		self.logger = logging.getLogger('main.engine.Engine')
		self.logger.debug('__init__ class Engine')

	def getLongPollServer(self):
		""" Get the longpoll server and set server, key, ts """
		
		response = self.sync_vk_request("groups.getLongPollServer", {'group_id': self.config['DEFAULT']['group_id']})
		
		if 'error' in response:
			self.logger.critical("getLongPollServer error: %s" % response)
			return 1

		self.__key, self.__server, self.__ts = response['response'].values()
		self.logger.debug("Get server, key, ts: %s %s %s" % (self.__server, self.__key, self.__ts))


	def requestLongPollServer(self):
		pass
