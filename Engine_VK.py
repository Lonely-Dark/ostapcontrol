#!/usr/bin/env python
# -*- coding: utf8 -*-

# ---Lonely_Dark---
# Python 3.9.6

import logging
from Requests import Requests

# Create registrator with name main.engine
module = logging.getLogger('main.engine')


class Engine(Requests):
    """ Engine for VK """

    def __init__(self):
        # Create registrator with name main.engine.Engine
        self.logger = logging.getLogger('main.engine.Engine')
        self.logger.debug('__init__ class Engine')

        # Requests.__init__()
        super().__init__()

    def get_long_poll_server(self):
        """ Get the longpoll server and set server, key, ts """

        response = self.sync_vk_request("groups.getLongPollServer",
                                        {"group_id":
                                         self.config['DEFAULT']['group_id']})

        if 'error' in response:
            self.logger.critical("getLongPollServer error: %s" % response)
            return 1

        self.__key, self.__server, self.ts = response['response'].values()
        self.logger.debug("Get server, key, ts: %s %s %s" %
                          (self.__server, self.__key, self.ts))

    def request_long_poll_server(self):
        """ Get event """
        self.event = self.sync_request(self.__server,
                                       {'act': 'a_check',
                                        'wait': 40,
                                        'key': self.__key,
                                        'ts': self.ts})


if __name__ == "__main__":
    module.setLevel(logging.DEBUG)
    module.addHandler(logging.StreamHandler())
    module.info("Using module as a main program")

    eng = Engine()
    eng.get_long_poll_server()
    eng.request_long_poll_server()
    module.debug(eng.event)
