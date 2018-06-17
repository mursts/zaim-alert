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


rgx = re.compile('\d{4}-\d{2}-\d{2}')


class ReceiveAPIHandler(webapp2.RequestHandler):
    def get(self):
        params = self.request.GET

        if 'date' not in params:
            self.response.status = 400
            self.response.write('Bad Request')
            return

        d = params['date']

        if not rgx.match(d):
            self.response.status = 400
            self.response.write('Bad Request')
            return

        receive_key = ndb.Key("Receive", d)
        receive = receive_key.get()

        if receive is None:
            self.response.status = 400
            self.response.write('Bad Request')
            return

        self.response.status = 200
        self.response.write(params['date'])


app = webapp2.WSGIApplication([
    ('/receive', ReceiveHandler),
    ('/api/receive', ReceiveAPIHandler),
], debug=False)
