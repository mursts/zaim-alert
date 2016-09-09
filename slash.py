#!/usr/bin/env python
# coding: utf-8

import logging
import urllib
from datetime import datetime, timedelta

import config
import webapp2
import zaim
from google.appengine.api import urlfetch


class Message(object):
    token = ""
    team_id = ""
    team_domain = ""
    channel_id = ""
    channel_name = ""
    user_id = ""
    user_name = ""
    command = ""
    text = ""
    response_url = ""
    args = []

    genre = ""
    amount = 0

    @classmethod
    def parse(cls, params):
        logging.debug(params)
        msg = cls()
        try:
            msg.token = params["token"]
            msg.team_id = params["team_id"]
            msg.team_domain = params["team_domain"]
            msg.channel_id = params["channel_id"]
            msg.channel_name = params["channel_name"]
            msg.user_id = params["user_id"]
            msg.user_name = params["user_name"]
            msg.text = params["text"]
            msg.response_url = params["response_url"]

            msg.args = msg.text.split()
            if len(msg.args) >= 3:
                msg.genre = msg.args[1]
                msg.amount = msg.args[2]
        except Exception, e:
            logging.error(e)
            raise e

        return msg


def response_message(response_url, text):
    payload = {'response_type': 'in_channel',
               'text': text}

    result = urlfetch.fetch(url=response_url,
                            payload=urllib.urlencode(payload),
                            method='POST')
    if result.status_code != 200:
        logging.error('{}: {}'.format(result.status_code, result.content))


class SlashHandler(webapp2.RequestHandler):
    def post(self):

        msg = Message.parse(self.request.POST)

        if not config.slack_slash_command_token == msg.token:
            logging.error('invalid token')
            return

        try:
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
            response_message(msg.response_url, e.message)

app = webapp2.WSGIApplication([
    ('/slash', SlashHandler)
], debug=False)
