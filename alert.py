#!/usr/bin/env python
# coding: utf-8

import json
from datetime import datetime, timedelta

import webapp2
from google.appengine.ext import ndb

from model import Receive # required

import config
import requests
import zaim


def notification():
    url = config.slack_imcoming_webhook_url
    text = {'text': '@mursts: zaimに:bento:の登録を忘れてますよ:face_with_rolling_eyes:',
            'attachments': [{'color': '#36a64f',
                             'title': '登録方法',
                             'text': '/zaim {category} amount\n■category\n  1: nanaco\n  2: Cach\n  3: QuickPay\n  4: Bento',
                             'fields': [{'short': False}]}]}

    payload = {'payload': json.dumps(text)}
    requests.post(url, data=payload)


class AlertHandler(webapp2.RequestHandler):
    def get(self):
        today = datetime.now() + timedelta(hours=9)

        receive_key = ndb.Key("Receive", today.strftime('%Y-%m-%d'))
        receive = receive_key.get()

        if receive is None:
            return

        api = zaim.Api(consumer_key=config.consumer_key, consumer_secret=config.consumer_secret,
                       access_token=config.access_token_key, access_token_secret=config.access_token_secret)

        money_list = api.money(mode='payment',
                               start_date=today.strftime('%Y-%m-%d'),
                               category_id=config.category)

        if len(money_list.get('money', [])) < 1:
            notification()


app = webapp2.WSGIApplication([
    ('/task/alert', AlertHandler)
], debug=False)