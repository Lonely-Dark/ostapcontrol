#!/usr/bin/env python
# -*- coding: utf8 -*-

# ---Lonely_Dark---
# Python 3.9.6

import logging
from Engine_VK import vk

main_logger = logging.getLogger('main')
main_logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("log.log")
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(fmt = '[%(asctime)s] [%(filename)s] [%(levelname)s] [%(lineno)d] [%(funcName)s]: %(message)s',datefmt = '%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

main_logger.addHandler(file_handler)
main_logger.addHandler(console_handler)

main_logger.info("Starting")

vk = vk()
vk.getLongPollServer()

running = True

while running:
	vk.requestLongPollServer()

	if len(vk.event['updates']) == 0:
		main_logger.debug("Updates 0, request to vk again...")
		continue

	main_logger.debug(vk.event)


	vk.ts = vk.event['ts']