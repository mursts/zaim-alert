#!/usr/bin/env python
# coding: utf-8

import calendar
import json
import logging
import sys
from datetime import datetime, timedelta, timezone

import requests
import zaim
from flask import Blueprint

import config
from datastore import get_client

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

task = Blueprint('alert', __name__, url_prefix='/task')


api = zaim.Api(consumer_key=config.consumer_key,
               consumer_secret=config.consumer_secret,
               access_token=config.access_token_key,
               access_token_secret=config.access_token_secret)


@task.route('/alert')
def alert_handler():
    jst = timezone(timedelta(hours=+9), 'JST')
    today = datetime.now(jst)

    ds_client = get_client()

    receive_key = ds_client.key('Receive', today.strftime('%Y-%m-%d'))
    receive = ds_client.get(receive_key)

    if receive is None:
        return 'OK'

    money_list = api.money(mode='payment',
                           start_date=today.strftime('%Y-%m-%d'),
                           category_id=config.category)

    if config.slack_imcoming_webhook_url != '' and len(money_list.get('money', [])) < 1:
        url = config.slack_imcoming_webhook_url
        text = {'text': '@mursts: zaimに:bento:の登録を忘れてますよ:face_with_rolling_eyes:'}

        payload = {'payload': json.dumps(text)}
        requests.post(url, data=payload)

    return 'OK'


@task.route('/report')
def report_handler():
    jst = timezone(timedelta(hours=+9), 'JST')
    today = datetime.now(jst)

    if not is_last_day_of_month(today):
        return 'OK'

    first_date = today.replace(day=1)
    _, month_days = calendar.monthrange(today.year, today.month)
    last_date = today.replace(day=month_days)

    money_list = api.money(mapping=1,
                           mode='payment',
                           start_date=first_date.strftime('%Y-%m-%d'),
                           end_date=last_date.strftime('%Y-%m-%d'))

    total_amount = 0
    payment_amount = 0
    report_list = []

    for money in money_list.get('money', []):
        amount = money.get('amount', 0)

        s = "{}:  {}".format(money.get('date')[5:], amount)
        total_amount += amount

        if is_payment(money.get('category_id'), money.get('genre_id')):
            payment_amount += amount
            s += "  *"

        report_list.append(s)

    report_list.sort()

    logger.debug(total_amount)
    logger.debug(payment_amount)
    logger.debug(report_list)

    text = u"""@mursts
{} のレポート

{}

*Total*
  `{} 円`

*うち振込分*
  `{} 円`
""".format(today.strftime('%Y/%m'), "\n".join(report_list), total_amount, payment_amount)

    url = config.slack_imcoming_webhook_url

    payload = {'payload': json.dumps({'text': text})}
    r = requests.post(url, data=payload)
    logger.debug(r.status_code)
    logger.debug(r.content)

    return 'OK'


def is_last_day_of_month(d):
    next_day = d + timedelta(days=1)
    return next_day.day == 1


def is_payment(category_id, genre_id) -> bool:
    return category_id == config.category and genre_id != config.genre_cash
