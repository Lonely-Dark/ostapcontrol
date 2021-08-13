#!/usr/bin/env python
# -*- coding: utf8 -*-

# ---Lonely_Dark---
# Python 3.9.6

from Requests import Requests
import logging
import sys
from io import StringIO
from traceback import format_exc
from Commands import Commands

# Create registrator with name main.handler
module = logging.getLogger("main.handler")


class Handler(Requests):

    def __init__(self):
        self.logger = logging.getLogger("main.handler.Handler")
        self.logger.debug("__init__ class Handler")
        self.commands = Commands()

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
        
        if 'action' in update[0]['object']['message']:
            self.action_handle(update[0]['object']['message']['action'])

        if len(self.text) == 0:
            return 0

        if str(self.peer_id) not in self.config:
            self.config[str(self.peer_id)] = {}
            temp = self.sync_vk_request("messages.getConversationMembers",
                                        {'peer_id': self.peer_id,
                                         'count': 200})
            if 'error' in temp:
                self.logger.debug("Error in tmp")
                self._handle()
            
            self.logger.debug(temp)

            temp = temp['response']['items']
            admins = []

            for i in range(len(temp)):
                if 'is_admin' in temp[i]:
                    admins.append(str(temp[i]['member_id']))

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

            self.commands.send_message(data, self.peer_id)

            sys.stdout, sys.stderr = out, error

        elif self.from_id != self.CREATOR and self.text_spl_lw[0] == 'py':
            self.commands.send_message('Не-не-не ты не создатель, я запрещаю',
                                       self.peer_id)

        if self.text_lw == 'остап админы':
            admins = self.config[str(self.peer_id)]['admins'].split()
            
            admins_users = [admins[i] for i in range(len(admins)) if int(admins[i]) > 0]
            admins_groups = [admins[i] for i in range(len(admins)) if int(admins[i]) < 0]
            admins_groups = [i[1:] for i in admins_groups]
            
            admins_users = ['@id'+admins_users[i]+'\n' for i in range(len(admins_users))]
            admins_groups = ['@public'+admins_groups[i]+'\n' for i in range(len(admins_groups))]
            
            self.commands.send_message(f"Админы юзеры:\n {''.join(admins_users)}\nАдмины группы:\n{''.join(admins_groups)}", self.peer_id)
        
    def action_handle(self, action):
        try:
            invite = self.config['invite_msg']
        except KeyError:
            invite = f"Приветствую @id{action['member_id']}, развлекайся!"

        if action['type'] == 'chat_invite_user':
            self.commands.send_message(invite, self.peer_id)


