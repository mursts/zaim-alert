#!/usr/bin/env python
# coding: utf-8

import json
import logging

from google.appengine.ext import ndb


class Receive(ndb.Model):
    pass


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
    def parse(cls, d):
        logging.debug(d)
        msg = cls()
        try:
            msg.token = d["token"]
            msg.team_id = d["team_id"]
            msg.team_domain = d["team_domain"]
            msg.channel_id = d["channel_id"]
            msg.channel_name = d["channel_name"]
            msg.user_id = d["user_id"]
            msg.user_name = d["user_name"]
            msg.command = d["command"]
            msg.text = d["text"]
            msg.response_url = d["response_url"]

            msg.args = msg.text.split()
            if len(msg.args) != 2:
                logging.error("text is {}".format(msg.args))
                raise ValueError("genre and amount are required")

            msg.genre = msg.args[0]
            msg.amount = msg.args[1]
        except Exception, e:
            logging.error(e)
            raise e

        return msg

    def jsonfy(self):
        return json.dumps({
            "token": self.token,
            "team_id":self.team_id,
            "team_domain": self.team_domain,
            "channel_id": self.channel_id,
            "channel_name": self.channel_name,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "command": self.command,
            "text": self.text,
            "response_url": self.response_url,
            "genre": self.genre,
            "amount": self.amount
        })

    @classmethod
    def load(cls, json_string):
        d = json.loads(json_string)

        msg = cls()
        msg.token = d["token"]
        msg.team_id = d["team_id"]
        msg.team_domain = d["team_domain"]
        msg.channel_id = d["channel_id"]
        msg.channel_name = d["channel_name"]
        msg.user_id = d["user_id"]
        msg.user_name = d["user_name"]
        msg.command = d["command"]
        msg.text = d["text"]
        msg.response_url = d["response_url"]
        msg.genre = d["genre"]
        msg.amount = d["amount"]

        return msg

