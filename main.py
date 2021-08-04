#!/usr/bin/env python
# -*- coding: utf8 -*-

# ---Lonely_Dark---
# Python 3.9.6

import logging
from Engine_VK import Engine
from Handler import Handler

# Create registrator with name main
main_logger = logging.getLogger('main')
main_logger.setLevel(logging.DEBUG)

# Create FileHandler for writing logs to log.log
file_handler = logging.FileHandler("log.log")
file_handler.setLevel(logging.DEBUG)

# Create StreamHandler for writing logs to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

fmt = '[%(asctime)s] [%(filename)s] [%(levelname)s] [%(lineno)d]: %(message)s'

# Set formatter to handlers
formatter = logging.Formatter(fmt=fmt, datefmt='%Y-%m-%d %H:%M:%S')

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to main_logger
main_logger.addHandler(file_handler)
main_logger.addHandler(console_handler)

main_logger.info("Starting")

vk = Engine()
handler = Handler()

vk.get_long_poll_server()

running = True

while running:
    vk.request_long_poll_server()

    # Check if events == 0
    if len(vk.event['updates']) == 0:
        main_logger.debug("Updates 0, request to vk again...")
        continue

    handler.handle(vk.event['updates'])

    vk.ts = vk.event['ts']

main_logger.info("Close the program")
