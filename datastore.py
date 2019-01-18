#!/usr/bin/env python
# coding: utf-8

import os

from google.cloud import datastore


def get_client():
    project_id = os.environ.get('DATASTORE_PROJECT_ID', None)
    if project_id:
        return datastore.Client(project=project_id)
    else:
        return datastore.Client()
