#!/usr/bin/env python
# coding: utf-8

import json
import logging
from datetime import datetime, timedelta

import webapp2
from google.appengine.api import urlfetch

import config
import zaim
from model import Message


def response_message(response_url, text):
    payload = {'response_type': 'in_channel',
               'text': text}

    result = urlfetch.fetch(url=response_url,
                            payload=json.dumps(payload),
                            method=urlfetch.POST)
    if result.status_code != 200:
        logging.error('{}: {}'.format(result.status_code, result.content))


class WorkerHandler(webapp2.RequestHandler):
    def post(self):
        msg_string = self.request.get("message")
        logging.debug(msg_string)

        msg = Message.load(msg_string)

        try:
            if not config.slack_slash_command_token == msg.token:
                logging.error('invalid token')
                return

            api = zaim.Api(consumer_key=config.consumer_key, consumer_secret=config.consumer_secret,
                           access_token=config.access_token_key, access_token_secret=config.access_token_secret)
            api.verify()

            today = datetime.now() + timedelta(hours=9)

            genres = dict([(genre['sort'], genre['id'])
                           for genre in api.genre()['genres']
                           if genre['category_id'] == config.category])

            response = api.payment(category_id=config.category,
                                   genre_id=genres[int(msg.genre)],
                                   amount=msg.amount,
                                   date=today.strftime('%Y-%m-%d'))

            logging.debug(response)
            response_message(msg.response_url, 'added.:+1:')

        except Exception, e:
            logging.error(e.message)
            response_message(msg.response_url, e.message)

app = webapp2.WSGIApplication([
    ('/task/messaging', WorkerHandler)
], debug=False)
