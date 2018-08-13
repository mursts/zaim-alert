#!/usr/bin/env python
# coding: utf-8

import calendar
import json
import logging
from datetime import datetime, timedelta

import webapp2
from pytz import timezone

import config
import requests
import zaim


class ReportHandler(webapp2.RequestHandler):
    def get(self):

        today = datetime.now(tz=timezone("Asia/Tokyo"))

        if not is_last_day_of_month(today):
            return

        first_date = today.replace(day=1)
        _, month_days = calendar.monthrange(today.year, today.month)
        last_date = today.replace(day=month_days)

        api = zaim.Api(consumer_key=config.consumer_key, consumer_secret=config.consumer_secret,
                       access_token=config.access_token_key, access_token_secret=config.access_token_secret)

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

            if is_payment_genre(money.get('genre_id')):
                payment_amount += amount
                s += "  *"

            report_list.append(s)

        report_list.sort()

        logging.debug(total_amount)
        logging.debug(payment_amount)

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
        logging.debug(r.status_code)
        logging.debug(r.content)


def is_last_day_of_month(d):
    next_day = d + timedelta(days=1)
    return next_day.day == 1


def is_payment_genre(genre_id):
    # 10763064:QuickPay
    # 15993748:COMP
    # 10914455:nanaco
    # 19777440:CalorieMate
    return genre_id in [10763064, 15993748, 10914455, 19777440]


app = webapp2.WSGIApplication([
    ('/task/report', ReportHandler)
], debug=False)
