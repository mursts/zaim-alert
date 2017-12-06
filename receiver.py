#!/usr/bin/env python
# coding: utf-8

import datetime

import webapp2

from model import Receive


class ReceiveHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("Receive Handler.")

        today = datetime.datetime.now() + datetime.timedelta(hours=9)
        receive = Receive(id=today.strftime('%Y-%m-%d'))
        receive.put()


app = webapp2.WSGIApplication([
    ('/receive', ReceiveHandler),
], debug=False)
