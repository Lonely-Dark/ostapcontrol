import requests
import logging
from configparser import ConfigParser

logging.basicConfig(format = '[%(asctime)s] [%(filename)s] [%(levelname)s] [%(lineno)d] [%(funcName)s]: %(message)s', level = logging.DEBUG, filename = "log.log")
logging.debug("Started.")

class Requests:
	
	def __init__(self, configname = "conf.ini", version = 5.131):
		if configname == "conf.ini" and version == 5.131:
			logging.info("Use default values for config name and version")

		self.config = ConfigParser()
		self.config.read(configname)
		self.params_update = {'access_token': self.config['DEFAULT']['token'], 'v': version}
	
	def sync_vk_request(self, method, parameters, update=True):
		if update:
			parameters.update(self.params_update)
			logging.debug("Parameters updated: %s" % parameters)

		return requests.get(f"https://api.vk.com/{method}", params=parameters)

	def sync_request(self, server, parameters):
		return requests.get(f"{server}", params=parameters)


class Engine(Requests):
	def getLongPollServer(self):
		""" Get the longpoll server and set server, key, ts """
		
		response = self.sync_vk_request("groups.getLongPollServer", {'group_id': self.config['DEFAULT']['group_id']})
		assert 'error' not in response, logging.critical("getLongPollServer error")
		__self.key, __self.server, __self.ts = response['response'].values()

#vk = Engine()