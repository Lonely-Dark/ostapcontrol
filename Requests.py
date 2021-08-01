#!/usr/bin/env python
# -*- coding: utf8 -*-

# ---Lonely_Dark---
# Python 3.9.6

import requests
import logging
from configparser import ConfigParser

# Create registrator with name requests
requests_logger = logging.getLogger('main.requests')

class Requests:
	
	def __init__(self, configname = "conf.ini", version = 5.131):
		
		# Create registrator with name requests.Requests
		self.logger = logging.getLogger('main.requests.Requests')

		# Parse config
		self.config = ConfigParser()
		self.config.read(configname)
		
		# Parameters update for sync_vk_request
		self.params_update = {'access_token': self.config['DEFAULT']['token'], 'v': version}

		if configname == "conf.ini" and version == 5.131:
			self.logger.info("Use default values for config name and version")
	
	def sync_vk_request(self, method, parameters, update=True):
		if update:
			parameters.update(self.params_update)
			self.logger.debug("Parameters updated: %s" % parameters)

		return requests.get(f"https://api.vk.com/method/{method}", params=parameters).json()

	def sync_request(self, server, parameters):
		return requests.get(server, params=parameters).json()

if __name__ == "__main__":
	requests_logger.debug("Using module as main program")
	requests_logger.debug("Create simple request to VK server")

	simple = Requests()
	trash = simple.sync_vk_request("users.get", {'user_ids': '186752691'})

	if 'error' in trash['response']:
		requests_logger.critical("Error in trash: %s" % trash)
	requests_logger.info("all clear.")