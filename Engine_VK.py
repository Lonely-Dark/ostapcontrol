import requests
from configparser import ConfigParser

class Requests:
	
	def __init__(self, configname="conf.ini", version=5.131):
		self.config = ConfigParser()
		self.config.read(configname)
		self.params_update = {'access_token': self.config['DEFAULT']['token'], 'v': version}
	
	def sync_vk_request(self, method, parameters, update=True):
		if update:
			parameters.update(self.params_update)
		return requests.get(f"https://api.vk.com/{method}", params=parameters)

	def sync_request(self, server, parameters):
		return requests.get(f"{server}", params=parameters)


class Engine(Requests):
	pass


vk = Engine("sorry.ini", 5.3131)