#!/usr/bin/env python
# coding: utf-8

import datetime
from logging import getLogger, StreamHandler, DEBUG

from flask import request, Blueprint, jsonify
from google.cloud import datastore

from datastore import get_client

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

receive = Blueprint('receive', __name__, url_prefix='/')
ds_client = get_client()


@receive.route('/receive')
def receive_hander():
    header = request.headers.get('X-LUNCH-ALERT', None)
    if header is None:
        return '', 200

    jst = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    today = datetime.datetime.now(jst)

    key = today.strftime('%Y-%m-%d')

    r = datastore.Entity(ds_client.key('Receive', key))
    ds_client.put(r)

    return 'Receive Handler.'


@receive.route('/api/receive')
def api_receive():
    params = request.args

    d = params.get('date')

    if d is None:
        return 'Bad Request', 400

    receive_key = ds_client.key('Receive', d)
    r = ds_client.get(receive_key)

    logger.debug(r)

    if r is None:
        logger.error(f'key{d} is not found.')
        return 'Bad Request', 400

    return jsonify({'date': d})
