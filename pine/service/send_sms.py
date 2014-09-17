# -*- coding: utf8 -*-
"""
 Copyright (C) 2008-2014 NURIGO
 http://www.coolsms.co.kr
"""
import sys
import os

sys.path.append("..")
from pine.util import coolsms


def send_msg(phone_num, gen_number):
    if os.environ['DJANGO_SETTINGS_MODULE'] == 'PineServerProject.settings.local':
        return

    api_key = 'NCS5402CEFE9E822'
    api_secret = '418AF75F20E3944A7A2772B3E59F83FB'
    to = phone_num
    sender = '3939'
    message = '[베일] ' + gen_number + ' 인증번호를 정확히 입력해주세요'
    cool = coolsms.rest(api_key, api_secret)
    status = cool.send(to, message, sender)