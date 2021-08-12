from Requests import Requests
from random import getrandbits


class Commands(Requests):

    def send_message(self, message, peer_id):
        self.sync_vk_request("messages.send",
                             {'random_id': getrandbits(64),
                              'peer_id': peer_id,
                              'message': message})
