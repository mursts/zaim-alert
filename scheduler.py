#! /usr/bin/env python
# coding: utf-8

import os
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from zaimapi import Zaim
from pushbullet import Pushbullet

sched = BlockingScheduler()

TARGET_GENRE = '会社ランチ'

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=12, minute=45)
def zaim_lunch_alert():
    consumer_key = os.environ.get("ZAIM_CONSUMER_KEY", None)
    consumer_secret = os.environ.get("ZAIM_CONSUMER_SECRET", "")
    access_token_key = os.environ.get("ZAIM_ACCESS_TOKEN_KEY", "")
    access_token_secret = os.environ.get("ZAIM_ACCESS_TOKEN_SECRET", "")

    pushbullet_token = os.environ.get('PUSHBULLET_TOKEN', "")
    target_device = os.environ.get('PUSHBULLET_TARGET_DEVICE', "")

    try:
        zaim = Zaim(consumer_key, consumer_secret, access_token_key, access_token_secret)

        genre = zaim.get_genre_by_name(TARGET_GENRE)
        genre_id = genre.get('id')

        today = datetime.today()

        params = {'start_date': today.strftime('%Y-%m-%d'),
                  'genre_id': genre_id}

        push_device = None
        pb = Pushbullet(pushbullet_token)
        for device in pb.devices:
            if device.model == target_device:
                push_device = device
                break
        else:
            raise ValueError('Device not found: ' + target_device)

        moeny_records = zaim.get_money_records(params)
        input_count = len(moeny_records)

        if input_count < 1:
            push = push_device.push_note('Zaim登録アラート', 'Zaimを登録！')

    except(Exception) as e:
        print(e)

sched.start()


