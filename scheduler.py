#! /usr/bin/env python
# coding: utf-8

import json
import os
import requests
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

from zaimapi import Zaim

sched = BlockingScheduler()

TARGET_GENRE_ID = ['6993487', '10763064', '10914455', '12506523']


def notification():
    url = os.environ.get('SLACK_WEBHOOK_URL', None)
    payload = {'payload': json.dumps({'text': '@mursts: zaimに:bento:の登録を忘れてますよ:face_with_rolling_eyes:'})}
    requests.post(url, data=payload)


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=12, minute=45)
def zaim_lunch_alert():
    consumer_key = os.environ.get("ZAIM_CONSUMER_KEY", None)
    consumer_secret = os.environ.get("ZAIM_CONSUMER_SECRET", None)
    access_token_key = os.environ.get("ZAIM_ACCESS_TOKEN_KEY", None)
    access_token_secret = os.environ.get("ZAIM_ACCESS_TOKEN_SECRET", None)

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
            notification()

    except Exception as e:
        print(e)

sched.start()


