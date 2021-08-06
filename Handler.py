#!/usr/bin/env python
# -*- coding: utf8 -*-

# ---Lonely_Dark---
# Python 3.9.6

from Requests import Requests
import logging
import sys
from io import StringIO
from traceback import format_exc
from random import getrandbits

# Create registrator with name main.handler
module = logging.getLogger("main.handler")


class Handler(Requests):

    def __init__(self):
        self.logger = logging.getLogger("main.handler.Handler")
        self.logger.debug("__init__ class Handler")

        super().__init__()

    def handle(self, update):
        self.logger.debug(update)
        self.type = update[0]['type']
        self.from_id = update[0]['object']['message']['from_id']
        self.peer_id = update[0]['object']['message']['peer_id']
        self.text = update[0]['object']['message']['text']
        self.text_spl = self.text.split()
        self.text_lw = self.text.lower()
        self.text_spl_lw = self.text_lw.split()

        if str(self.peer_id) not in self.config:
            self.config[str(self.peer_id)] = {}
            temp = self.sync_vk_request("messages.getConversationMembers",
                                        {'peer_id': self.peer_id,
                                         'count': 200})
            if 'error' in temp:
                self.logger.debug("Error in tmp")
                self._handle()
            self.logger.debug(temp)
            admins = [temp['response']['items'][i]['member_id'] for i in range(len(temp['response']['items'])) if 'is_admin' in temp['response']['items'][i]]
            admins = list(map(str, admins))
            self.logger.debug(admins)
            self.config[str(self.peer_id)]['admins'] = ' '.join(admins)

            with open("conf.ini", "w") as file:
                self.config.write(file)

        self._handle()

    def _handle(self):
        if self.from_id == self.CREATOR and self.text_spl_lw[0] == 'py':
            out, error = sys.stdout, sys.stderr
            code_to_run = ' '.join(self.text_spl[1:])
            sys.stdout = StringIO()
            sys.stderr = sys.stdout

            try:
                exec(code_to_run)
            except:
                sys.stdout.write(format_exc())

            sys.stdout.seek(0)
            data = sys.stdout.read()

            self.sync_vk_request("messages.send",
                                 {'random_id': getrandbits(64),
                                  'peer_id': self.peer_id, 'message': data})

            sys.stdout, sys.stderr = out, error
