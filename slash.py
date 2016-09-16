#!/usr/bin/env python
# coding: utf-8

import webapp2
from google.appengine.api import taskqueue

from model import Message


class SlashHandler(webapp2.RequestHandler):
    def post(self):
        msg = Message.parse(self.request.POST)
        # queueに投げるだけ
        taskqueue.add(url='/task/messaging',
                      target='default',
                      params={'message': msg.jsonfy()})

app = webapp2.WSGIApplication([
    ('/slash', SlashHandler)
], debug=False)
