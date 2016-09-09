#!/usr/bin/env python
# coding: utf-8

import json
from datetime import datetime, timedelta

import webapp2

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
    def post(self):
        api = zaim.Api(consumer_key=config.consumer_key, consumer_secret=config.consumer_secret,
                       access_token=config.access_token_key, access_token_secret=config.access_token_secret)

        genres = [genre['id'] for genre in api.genre()['genres'] if genre['category_id'] == config.category]

        today = datetime.now() + timedelta(hours=9)

        money_list = api.money(mapping=1,
                               mode='payment',
                               start_date=today.strftime('%Y-%m-%d'))

        for money in money_list.get('money', []):
            if money['genre_id'] in genres:
                break
        else:
            notification()


app = webapp2.WSGIApplication([
    ('/task/alert', AlertHandler)
], debug=False)