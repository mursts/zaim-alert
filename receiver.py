#!/usr/bin/env python
# coding: utf-8

import datetime
import re

import webapp2
from google.appengine.ext import ndb

from model import Receive


class ReceiveHandler(webapp2.RequestHandler):
    def get(self):
        header = self.request.headers.get("X-LUNCH-ALERT", None)
        if header is None:
            return

        self.response.write("Receive Handler.")

        today = datetime.datetime.now() + datetime.timedelta(hours=9)
        receive = Receive(id=today.strftime('%Y-%m-%d'))
        receive.put()


class ReceiveAPIHandler(webapp2.RequestHandler):
    def get(self):
        params = self.request.GET

        try:
            if 'date' not in params:
                raise ValueError

            d = params['date']

            receive_key = ndb.Key("Receive", d)
            receive = receive_key.get()

            if receive is None:
                raise ValueError

            self.response.status = 200
            self.response.write(params['date'])

        except ValueError:
            self.response.status = 400
            self.response.write('Bad Request')


app = webapp2.WSGIApplication([
    ('/receive', ReceiveHandler),
    ('/api/receive', ReceiveAPIHandler),
], debug=False)
