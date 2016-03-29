#! /usr/bin/env python
# coding: utf-8

import os
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from pushbullet import Pushbullet

from zaimapi import Zaim

sched = BlockingScheduler()

# 会社ランチ, 会社ランチ(QuickPay)
TARGET_GENRE_ID = ['6993487', '10763064', '10914455']

pushbullet_token = os.environ.get('PUSHBULLET_TOKEN', "")
target_device = os.environ.get('PUSHBULLET_TARGET_DEVICE', "")


def get_device():
    pb = Pushbullet(pushbullet_token)
    for device in pb.devices:
        if device.model == target_device:
            return device
    else:
        raise ValueError('Device not found: ' + target_device)


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=12, minute=45)
def zaim_lunch_alert():
    consumer_key = os.environ.get("ZAIM_CONSUMER_KEY", None)
    consumer_secret = os.environ.get("ZAIM_CONSUMER_SECRET", "")
    access_token_key = os.environ.get("ZAIM_ACCESS_TOKEN_KEY", "")
    access_token_secret = os.environ.get("ZAIM_ACCESS_TOKEN_SECRET", "")

    try:
        zaim = Zaim(consumer_key, consumer_secret, access_token_key, access_token_secret)

        today = datetime.today()

        params = {'start_date': today.strftime('%Y-%m-%d')}

        money_records = zaim.get_money_records(params)

        for record in money_records:
            genre_id = str(record.get('genre_id'))
            if genre_id in TARGET_GENRE_ID:
                break
        else:
            device = get_device()
            device.push_note('Zaim登録アラート', 'Zaimを登録！')

    except Exception as e:
        print(e)

sched.start()


